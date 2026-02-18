"""
Browser automation for Panorama SSO authentication and page interaction.

Uses Playwright persistent browser profiles so that cookies, cache, and session
state survive across browser restarts.  When a Panorama session expires the
module automatically clicks "Use Single Sign-On" to re-authenticate via the
identity provider without user interaction (as long as the IDP session is alive).
"""

import asyncio
import json
import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from playwright.async_api import (
    async_playwright,
    BrowserContext,
    Page,
    Playwright,
)


# ---------------------------------------------------------------------------
# Profile storage
# ---------------------------------------------------------------------------
CONFIG_DIR = Path.home() / ".config" / "panorama-mcp"
PROFILES_DIR = CONFIG_DIR / "profiles"


def _instance_key(url: str) -> str:
    """Derive a filesystem-safe key from a Panorama URL."""
    hostname = urlparse(url).hostname or url
    return hostname.replace(".", "_")


def _profile_dir(url: str) -> Path:
    """Chromium profile directory for a given instance."""
    return PROFILES_DIR / _instance_key(url)


def is_session_valid(url: str) -> bool:
    """
    Check if a persistent profile exists for this instance.

    With persistent profiles the real session validity is determined
    server-side.  This just tells us if a login has happened at all.
    """
    profile = _profile_dir(url)
    if not profile.exists():
        return False
    # A profile dir with >0 files means Chromium has written state
    try:
        return any(profile.iterdir())
    except Exception:
        return False


# Common IDP domains
_IDP_INDICATORS = [
    "okta", "microsoftonline", "login.microsoft", "adfs", "ping",
    "auth0", "onelogin", "duo", "azure", "google.com/accounts",
    "sso.", "idp.", "identity.", "federation", "saml", "sts.",
    "login.windows.net",
]

# Panorama UI selectors that confirm a logged-in session
_PANORAMA_NAV_SELECTORS = [
    "#dashboard", ".pan-dashboard", "#topNav", ".device-tab",
    "#acc-management", ".dashboard-widget",
    'text="Dashboard"', 'text="ACC"', 'text="Monitor"',
    'text="Policies"', 'text="Objects"', 'text="Network"',
    'text="Device"', 'text="Panorama"',
]


# ---------------------------------------------------------------------------
# PanoramaSession
# ---------------------------------------------------------------------------
@dataclass
class PanoramaSession:
    """Manages a Playwright persistent browser context for one Panorama instance."""

    panorama_url: str
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None
    playwright: Optional[Playwright] = None
    is_authenticated: bool = False

    @property
    def instance_name(self) -> str:
        return urlparse(self.panorama_url).hostname or self.panorama_url

    @property
    def profile_path(self) -> Path:
        return _profile_dir(self.panorama_url)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    async def initialize(self, headless: bool = False) -> None:
        """Start browser with a persistent Chromium profile."""
        self.profile_path.mkdir(parents=True, exist_ok=True)

        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_path),
            headless=headless,
            channel="msedge",  # use system Edge (has corp certs & proxy)
            viewport={"width": 1920, "height": 1080},
            args=["--disable-blink-features=AutomationControlled"],
        )
        # Persistent contexts open with one blank page
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        self.page.set_default_timeout(30000)

    async def close(self) -> None:
        """Tear down browser resources."""
        if self.context:
            try:
                await self.context.close()
            except Exception:
                pass
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception:
                pass
        self.page = self.context = self.playwright = None

    # ------------------------------------------------------------------
    # Login detection
    # ------------------------------------------------------------------
    def _is_on_idp_page(self) -> bool:
        """True if the browser is on an identity-provider page."""
        try:
            url = self.page.url.lower()
            if self.instance_name.lower() in url:
                return False
            return any(idp in url for idp in _IDP_INDICATORS)
        except Exception:
            return False

    async def _is_on_panorama_login(self) -> bool:
        """True if the page is the Panorama local login page.

        Panorama uses login.php as the base URL even when authenticated
        (hash routing: login.php?...#dashboard).  So we check for the
        actual login form elements rather than just 'login' in the URL.
        Uses JS query for speed (no waiting/timeout).
        """
        if not self.page:
            return False
        try:
            url = self.page.url.lower()
            host = self.instance_name.lower()
            if host not in url:
                return False
            # Fast JS check for login form elements — no waiting
            return await self.page.evaluate("""() => {
                const selectors = [
                    'input[name="user"]', 'input[name="passwd"]',
                    '#loginForm', 'input[type="password"]'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el && el.offsetParent !== null) return true;
                }
                // Check for SSO link text
                const links = document.querySelectorAll('a');
                for (const a of links) {
                    const text = (a.textContent || '').toLowerCase();
                    if (text.includes('single sign') || text.includes('sso')) {
                        if (a.offsetParent !== null) return true;
                    }
                }
                return false;
            }""")
        except Exception:
            return False

    async def _is_logged_in_on_current_page(self) -> bool:
        """
        Does the current page indicate an authenticated Panorama session?

        Uses a single fast JS call to check for dashboard elements,
        rather than trying selectors one-by-one with timeouts.
        Dashboard elements trump URL-based login detection (Panorama
        uses login.php as the base URL even when authenticated).
        """
        if not self.page:
            return False
        try:
            url = self.page.url.lower()
            host = self.instance_name.lower()

            if self._is_on_idp_page():
                return False
            if host not in url:
                return False

            # Single JS call to check all nav selectors at once (fast)
            has_dashboard = await self.page.evaluate("""() => {
                // CSS selectors
                const cssSelectors = [
                    '#dashboard', '.pan-dashboard', '#topNav', '.device-tab',
                    '#acc-management', '.dashboard-widget'
                ];
                for (const sel of cssSelectors) {
                    if (document.querySelector(sel)) return true;
                }
                // Text-based checks
                const navTexts = ['Dashboard', 'ACC', 'Monitor', 'Policies',
                                  'Objects', 'Network', 'Device', 'Panorama'];
                const allText = document.body ? document.body.innerText : '';
                let matches = 0;
                for (const t of navTexts) {
                    if (allText.includes(t)) matches++;
                }
                // Need at least 3 nav items to confirm dashboard
                return matches >= 3;
            }""")

            if has_dashboard:
                return True

            # No dashboard elements — check if on actual login form
            if await self._is_on_panorama_login():
                return False

            # On Panorama host, no dashboard, no login form —
            # page may still be loading; treat as authenticated
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Popup dismissal (e.g., "What's New" after Panorama upgrades)
    # ------------------------------------------------------------------
    async def dismiss_popups(self) -> None:
        """Detect and close common Panorama popups / modals."""
        if not self.page:
            return
        popup_dismiss_selectors = [
            # "What's New" / release notes popup
            'button:has-text("Close")',
            'button:has-text("Got It")',
            'button:has-text("OK")',
            'button:has-text("Dismiss")',
            'button:has-text("Don\'t show")',
            'button:has-text("Save")',
            # Generic modal close buttons
            '.modal .close', '.dialog .close',
            'button.pan-btn-close', '.modal-close',
            '[aria-label="Close"]', '[aria-label="close"]',
            '.whatsnew button', '#whatsnew-close',
            '.release-notes button',
        ]
        for sel in popup_dismiss_selectors:
            try:
                el = await self.page.wait_for_selector(sel, timeout=1500)
                if el and await el.is_visible():
                    await el.click()
                    await asyncio.sleep(1)
            except Exception:
                continue

    # ------------------------------------------------------------------
    # Auto-SSO flow
    # ------------------------------------------------------------------
    async def _fill_sso_account_and_continue(self) -> bool:
        """
        If on the SSO Account page, fill the account field and click
        Continue.  Uses PANORAMA_SSO_ACCOUNT env var.
        """
        sso_account = os.environ.get("PANORAMA_SSO_ACCOUNT", "").strip()
        if not sso_account:
            return False

        try:
            title = (await self.page.title()).lower()
            # Detect the SSO Account intermediate page
            is_sso_page = "single sign" in title or "sso" in title
            if not is_sso_page:
                # Also check for the SSO Account input directly
                try:
                    await self.page.wait_for_selector(
                        'input[placeholder*="SSO"], input[name*="sso"], '
                        'input[id*="sso"], input[placeholder*="Account"]',
                        timeout=2000,
                    )
                    is_sso_page = True
                except Exception:
                    pass

            if not is_sso_page:
                return False

            # Find and fill the SSO account input
            input_selectors = [
                'input[placeholder*="SSO Account"]',
                'input[placeholder*="SSO"]',
                'input[placeholder*="Account"]',
                'input[name*="sso"]',
                'input[id*="sso"]',
                'input[type="text"]',  # fallback: first text input on page
            ]
            filled = False
            for sel in input_selectors:
                try:
                    inp = await self.page.wait_for_selector(sel, timeout=2000)
                    if inp and await inp.is_visible():
                        await inp.fill(sso_account)
                        filled = True
                        break
                except Exception:
                    continue

            if not filled:
                return False

            # Click Continue
            continue_selectors = [
                'button:has-text("Continue")',
                'input[type="submit"]',
                'button[type="submit"]',
            ]
            for sel in continue_selectors:
                try:
                    btn = await self.page.wait_for_selector(sel, timeout=2000)
                    if btn and await btn.is_visible():
                        await btn.click()
                        return True
                except Exception:
                    continue

            return False
        except Exception:
            return False

    async def _try_auto_sso(self, timeout: int = 45) -> bool:
        """
        Handle the full SSO flow automatically:
        1. Click "Use Single Sign-On" on the main login page
        2. Fill SSO Account + click Continue on the SSO page
        3. Wait for IDP to redirect back (using saved IDP cookies)
        """
        if not self.page:
            return False
        try:
            # Step 1: Click "Use Single Sign-On" if on the main login page
            sso_link_selectors = [
                'a:has-text("Single Sign-On")',
                'a:has-text("Use Single Sign")',
                'a:has-text("SSO")',
                'a[href*="saml"]',
                '#sso_login',
            ]
            for sel in sso_link_selectors:
                try:
                    link = await self.page.wait_for_selector(sel, timeout=2000)
                    if link and await link.is_visible():
                        await link.click()
                        await asyncio.sleep(2)
                        break
                except Exception:
                    continue

            # Step 2: Handle SSO Account page
            await self._fill_sso_account_and_continue()
            await asyncio.sleep(3)

            # Step 3: Wait for IDP redirect chain to complete
            start = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start < timeout:
                await asyncio.sleep(2)
                try:
                    await self.page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass

                # Made it back to Panorama?
                if await self._is_logged_in_on_current_page():
                    self.is_authenticated = True
                    await self.dismiss_popups()
                    return True

                # Still on IDP — keep waiting (IDP may auto-submit)
                if self._is_on_idp_page():
                    continue

                # Back on Panorama login/SSO page — IDP session expired
                if await self._is_on_panorama_login():
                    return False

            return False
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Public auth check
    # ------------------------------------------------------------------
    async def check_login_status(self, auto_sso: bool = True) -> bool:
        """Navigate to instance and check/restore authentication.

        Args:
            auto_sso: If True, attempt automatic SSO re-auth when on login page.
                      Set to False to just check without triggering any auth flow.
        """
        if not self.page:
            return False
        try:
            await self.page.goto(
                self.panorama_url,
                wait_until="networkidle",
                timeout=30000,
            )
            await asyncio.sleep(3)

            # Already authenticated?
            if await self._is_logged_in_on_current_page():
                self.is_authenticated = True
                await self.dismiss_popups()
                return True

            if not auto_sso:
                return False

            # On login page or SSO account page — try silent SSO re-auth
            if await self._is_on_panorama_login():
                result = await self._try_auto_sso()
                if result:
                    await self.dismiss_popups()
                return result

            # Check if on the SSO Account page specifically (title-based)
            try:
                title = (await self.page.title()).lower()
                if "single sign" in title or "sso" in title:
                    result = await self._try_auto_sso()
                    if result:
                        await self.dismiss_popups()
                    return result
            except Exception:
                pass

            # On IDP page — IDP might auto-submit; wait briefly
            if self._is_on_idp_page():
                for _ in range(15):
                    await asyncio.sleep(2)
                    try:
                        await self.page.wait_for_load_state("networkidle", timeout=5000)
                    except Exception:
                        pass
                    if await self._is_logged_in_on_current_page():
                        self.is_authenticated = True
                        return True
                return False

            return False
        except Exception:
            return False

    # ------------------------------------------------------------------
    # SSO login (async, for MCP tool calls)
    # ------------------------------------------------------------------
    async def wait_for_sso_login(self, timeout_seconds: int = 300) -> dict:
        """Open visible browser and wait for SSO completion."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        await self.page.goto(self.panorama_url, wait_until="domcontentloaded")

        # Try auto-SSO first
        if await self._is_on_panorama_login():
            if await self._try_auto_sso(timeout=60):
                return {
                    "success": True,
                    "message": "Auto-SSO re-authenticated successfully",
                    "instance": self.instance_name,
                }

        start = asyncio.get_event_loop().time()
        while True:
            elapsed = asyncio.get_event_loop().time() - start
            if elapsed > timeout_seconds:
                return {
                    "success": False,
                    "error": f"SSO login timed out after {timeout_seconds}s",
                    "hint": "Run 'panorama-mcp login' in a terminal for interactive auth",
                }
            if await self._is_logged_in_on_current_page():
                self.is_authenticated = True
                return {
                    "success": True,
                    "message": "SSO login completed, session persisted in browser profile",
                    "instance": self.instance_name,
                }
            await asyncio.sleep(2)

    # ------------------------------------------------------------------
    # Page helpers
    # ------------------------------------------------------------------
    async def navigate_to_panorama(self) -> dict:
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.goto(self.panorama_url, wait_until="networkidle")
        return await self.get_page_info()

    async def get_page_info(self) -> dict:
        if not self.page:
            return {"error": "Browser not initialized"}
        return {"url": self.page.url, "title": await self.page.title()}

    async def take_screenshot(self, path: Optional[str] = None) -> bytes:
        if not self.page:
            raise RuntimeError("Browser not initialized")
        if path:
            return await self.page.screenshot(path=path)
        return await self.page.screenshot()

    async def get_page_snapshot(self) -> str:
        if not self.page:
            raise RuntimeError("Browser not initialized")
        # Playwright >= 1.49 removed page.accessibility; use locator.aria_snapshot()
        try:
            snapshot = await self.page.locator("body").aria_snapshot()
            return snapshot if snapshot else "{}"
        except AttributeError:
            # Fallback for older Playwright versions
            snapshot = await self.page.accessibility.snapshot()
            return json.dumps(snapshot, indent=2) if snapshot else "{}"

    async def click_element(self, selector: str) -> dict:
        if not self.page:
            raise RuntimeError("Browser not initialized")
        try:
            await self.page.click(selector)
            await self.page.wait_for_load_state("networkidle")
            return {"success": True, "message": f"Clicked: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def fill_input(self, selector: str, value: str) -> dict:
        if not self.page:
            raise RuntimeError("Browser not initialized")
        try:
            await self.page.fill(selector, value)
            return {"success": True, "message": f"Filled: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_table_data(self, table_selector: str) -> list[dict]:
        if not self.page:
            raise RuntimeError("Browser not initialized")
        try:
            headers = await self.page.eval_on_selector_all(
                f"{table_selector} thead th",
                "elements => elements.map(el => el.textContent.trim())",
            )
            rows = await self.page.eval_on_selector_all(
                f"{table_selector} tbody tr",
                """rows => rows.map(row => {
                    const cells = row.querySelectorAll('td');
                    return Array.from(cells).map(cell => cell.textContent.trim());
                })""",
            )
            result = []
            for row in rows:
                if len(row) == len(headers):
                    result.append(dict(zip(headers, row)))
                else:
                    result.append({"raw_data": row})
            return result
        except Exception as e:
            return [{"error": str(e)}]


# ---------------------------------------------------------------------------
# Multi-instance session manager
# ---------------------------------------------------------------------------
_sessions: dict[str, PanoramaSession] = {}


async def get_session(
    panorama_url: str, headless: bool = False
) -> PanoramaSession:
    """Get or create a session for a Panorama instance."""
    key = _instance_key(panorama_url)
    session = _sessions.get(key)
    if session is None:
        session = PanoramaSession(panorama_url=panorama_url)
        await session.initialize(headless=headless)
        _sessions[key] = session
    return session


async def ensure_authenticated(
    panorama_url: str, headless: bool = False
) -> PanoramaSession:
    """
    Get a session and ensure it is authenticated.

    If not authenticated, runs auto-SSO.  If auto-SSO needs user interaction
    (MFA), waits for the user to press ENTER in the terminal.

    The session is kept alive — Panorama uses session-only cookies that are
    destroyed when the browser closes.
    """
    session = await get_session(panorama_url, headless=headless)

    # Check current auth status
    auth = await session.check_login_status(auto_sso=True)
    if auth:
        return session

    # Auto-SSO got to IDP but needs user interaction
    if session.page and session._is_on_idp_page():
        import sys

        print(f"\n  {'='*56}", file=sys.stderr)
        print("  Complete SSO login in the browser window.", file=sys.stderr)
        print("  Once you see the Panorama dashboard, press ENTER here.", file=sys.stderr)
        print("  (Ctrl+C to cancel)", file=sys.stderr)
        print(f"  {'='*56}\n", file=sys.stderr)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, input, "  Press ENTER when login is complete... "
        )
        await asyncio.sleep(2)

        # Re-navigate to Panorama
        await session.page.goto(panorama_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        if await session._is_logged_in_on_current_page():
            session.is_authenticated = True
            await session.dismiss_popups()

    return session


async def close_session(panorama_url: str) -> None:
    """Close a specific instance session."""
    key = _instance_key(panorama_url)
    session = _sessions.pop(key, None)
    if session:
        await session.close()


async def close_all_sessions() -> None:
    """Close all sessions."""
    for session in list(_sessions.values()):
        await session.close()
    _sessions.clear()


def clear_saved_session(panorama_url: str) -> None:
    """Delete the persistent profile for an instance."""
    profile = _profile_dir(panorama_url)
    if profile.exists():
        shutil.rmtree(profile, ignore_errors=True)


# ---------------------------------------------------------------------------
# Synchronous interactive login (for CLI pre-auth)
# ---------------------------------------------------------------------------
def login_interactive_sync(panorama_url: str) -> None:
    """
    Blocking interactive login for CLI usage.

    Opens a visible browser with a persistent profile, lets the user
    complete SSO, waits for ENTER, then closes the browser.  The profile
    retains all cookies and state for headless reuse.
    """
    from playwright.sync_api import sync_playwright

    profile = _profile_dir(panorama_url)
    profile.mkdir(parents=True, exist_ok=True)
    instance_host = urlparse(panorama_url).hostname.lower()

    pw = sync_playwright().start()
    context = pw.chromium.launch_persistent_context(
        user_data_dir=str(profile),
        headless=False,
        channel="msedge",  # use system Edge (has corp certs & proxy)
        viewport={"width": 1920, "height": 1080},
        args=["--disable-blink-features=AutomationControlled"],
    )

    # Track popup windows (some IDPs open auth in a new window)
    all_pages = list(context.pages)

    def _on_new_page(new_page):
        all_pages.append(new_page)
        print(f"  [popup opened] {new_page.url}")

    context.on("page", _on_new_page)

    page = all_pages[0] if all_pages else context.new_page()

    try:
        page.goto(panorama_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)

        # Check: already authenticated from persistent profile?
        current_url = page.url.lower()
        already_authed = False
        if instance_host in current_url and "login" not in current_url:
            for sel in _PANORAMA_NAV_SELECTORS:
                try:
                    el = page.wait_for_selector(sel, timeout=3000)
                    if el:
                        already_authed = True
                        break
                except Exception:
                    continue

        if already_authed:
            print("Already authenticated from saved profile!")
            return

        # On login page — click SSO link to start the flow
        if "login" in page.url.lower():
            sso_link_selectors = [
                'a:has-text("Single Sign-On")',
                'a:has-text("Use Single Sign")',
                'a:has-text("SSO")',
            ]
            for sel in sso_link_selectors:
                try:
                    link = page.wait_for_selector(sel, timeout=2000)
                    if link and link.is_visible():
                        print("Clicking 'Use Single Sign-On'...")
                        link.click()
                        try:
                            page.wait_for_load_state("networkidle", timeout=10000)
                        except Exception:
                            pass
                        break
                except Exception:
                    continue

        # Fill SSO Account field if env var is set
        sso_account = os.environ.get("PANORAMA_SSO_ACCOUNT", "").strip()
        if sso_account:
            title = page.title().lower()
            if "single sign" in title or "sso" in title:
                sso_input_selectors = [
                    'input[placeholder*="SSO Account"]',
                    'input[placeholder*="SSO"]',
                    'input[placeholder*="Account"]',
                    'input[type="text"]',
                ]
                for sel in sso_input_selectors:
                    try:
                        inp = page.wait_for_selector(sel, timeout=2000)
                        if inp and inp.is_visible():
                            print(f"Filling SSO Account: {sso_account}")
                            # Clear and type (not fill) to trigger JS events
                            inp.click()
                            inp.fill("")
                            page.keyboard.type(sso_account, delay=50)
                            time.sleep(1)
                            # Click Continue and wait for navigation
                            for btn_sel in ['button:has-text("Continue")',
                                            'input[type="submit"]',
                                            'button[type="submit"]']:
                                try:
                                    btn = page.wait_for_selector(btn_sel, timeout=2000)
                                    if btn and btn.is_visible():
                                        print("  Clicking Continue...")
                                        btn.click()
                                        print("  Waiting for SSO redirect...")
                                        try:
                                            page.wait_for_url(
                                                lambda u: "login.php" not in u,
                                                timeout=15000,
                                            )
                                        except Exception:
                                            pass
                                        break
                                except Exception:
                                    continue
                            break
                    except Exception:
                        continue

        # Show where we are (non-blocking — page.url is a property, not a call)
        print(f"  Current URL: {page.url}")

        # Always wait for user to confirm — never auto-close
        print(f"\n{'='*60}")
        print("Complete SSO login in the browser window.")
        print("Once you see the Panorama dashboard, press ENTER here.")
        print("(Ctrl+C to cancel)")
        print(f"{'='*60}\n")

        try:
            input("Press ENTER when login is complete... ")
        except KeyboardInterrupt:
            raise RuntimeError("Login cancelled by user")

        time.sleep(2)
        print("Session saved in browser profile!")

    finally:
        context.close()
        pw.stop()
