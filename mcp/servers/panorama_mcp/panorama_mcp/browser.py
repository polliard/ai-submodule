"""
Browser automation module for Panorama SSO authentication and page interaction.

Uses Playwright for browser automation to handle SSO login flows and
screen scraping when API access is not available.
"""

import asyncio
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright


@dataclass
class PanoramaSession:
    """Manages a browser session for Panorama."""
    panorama_url: str
    browser: Optional[Browser] = None
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None
    playwright: Optional[Playwright] = None
    is_authenticated: bool = False
    storage_path: Path = field(default_factory=lambda: Path.home() / ".panorama_mcp" / "auth_state.json")

    async def initialize(self, headless: bool = False) -> None:
        """Initialize the browser with optional saved auth state."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)

        # Try to load saved auth state
        if self.storage_path.exists():
            try:
                self.context = await self.browser.new_context(
                    storage_state=str(self.storage_path)
                )
                self.is_authenticated = True
            except Exception:
                self.context = await self.browser.new_context()
        else:
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

        # Set reasonable timeout
        self.page.set_default_timeout(30000)

    async def save_auth_state(self) -> None:
        """Save authentication state for future sessions."""
        if self.context:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            await self.context.storage_state(path=str(self.storage_path))
            self.is_authenticated = True

    async def navigate_to_panorama(self) -> dict:
        """Navigate to Panorama main page."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        await self.page.goto(self.panorama_url, wait_until="networkidle")
        return await self.get_page_info()

    async def check_login_status(self) -> bool:
        """Check if currently logged into Panorama."""
        if not self.page:
            return False

        try:
            # Check for common Panorama logged-in indicators
            # Panorama typically shows user info or dashboard when logged in
            await self.page.goto(self.panorama_url, wait_until="networkidle")

            # Look for login page indicators
            login_indicators = [
                'input[name="user"]',
                'input[name="passwd"]',
                '#loginForm',
                'text="Sign in"',
                'text="Log In"'
            ]

            for indicator in login_indicators:
                try:
                    element = await self.page.wait_for_selector(indicator, timeout=2000)
                    if element:
                        return False  # Found login page element
                except:
                    pass

            # Check for dashboard/logged-in indicators
            dashboard_indicators = [
                '#dashboard',
                '.pan-dashboard',
                'text="Dashboard"',
                'text="Devices"',
                '#topNav'
            ]

            for indicator in dashboard_indicators:
                try:
                    element = await self.page.wait_for_selector(indicator, timeout=2000)
                    if element:
                        return True  # Found logged-in element
                except:
                    pass

            return False
        except Exception:
            return False

    async def wait_for_sso_login(self, timeout_seconds: int = 300) -> dict:
        """
        Wait for user to complete SSO login manually.

        Opens browser and waits for user to authenticate through SSO provider.
        Returns success status and saves auth state for future use.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")

        # Navigate to Panorama
        await self.page.goto(self.panorama_url, wait_until="networkidle")

        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout_seconds:
                return {
                    "success": False,
                    "error": "SSO login timeout",
                    "message": f"Login not completed within {timeout_seconds} seconds"
                }

            # Check if we're now logged in
            if await self.check_login_status():
                await self.save_auth_state()
                return {
                    "success": True,
                    "message": "SSO login completed successfully",
                    "panorama_url": self.panorama_url
                }

            await asyncio.sleep(2)

    async def get_page_info(self) -> dict:
        """Get current page information."""
        if not self.page:
            return {"error": "Browser not initialized"}

        return {
            "url": self.page.url,
            "title": await self.page.title()
        }

    async def take_screenshot(self, path: Optional[str] = None) -> bytes:
        """Take a screenshot of the current page."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        if path:
            return await self.page.screenshot(path=path)
        return await self.page.screenshot()

    async def get_page_snapshot(self) -> str:
        """Get accessibility tree snapshot of the page (for AI interaction)."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        # Get accessibility snapshot
        snapshot = await self.page.accessibility.snapshot()
        return json.dumps(snapshot, indent=2) if snapshot else "{}"

    async def click_element(self, selector: str) -> dict:
        """Click an element on the page."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        try:
            await self.page.click(selector)
            await self.page.wait_for_load_state("networkidle")
            return {"success": True, "message": f"Clicked element: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def fill_input(self, selector: str, value: str) -> dict:
        """Fill an input field."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        try:
            await self.page.fill(selector, value)
            return {"success": True, "message": f"Filled input: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_table_data(self, table_selector: str) -> list[dict]:
        """Extract data from an HTML table."""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        try:
            # Get headers
            headers = await self.page.eval_on_selector_all(
                f"{table_selector} thead th",
                "elements => elements.map(el => el.textContent.trim())"
            )

            # Get rows
            rows = await self.page.eval_on_selector_all(
                f"{table_selector} tbody tr",
                """rows => rows.map(row => {
                    const cells = row.querySelectorAll('td');
                    return Array.from(cells).map(cell => cell.textContent.trim());
                })"""
            )

            # Combine headers with data
            result = []
            for row in rows:
                if len(row) == len(headers):
                    result.append(dict(zip(headers, row)))
                else:
                    result.append({"raw_data": row})

            return result
        except Exception as e:
            return [{"error": str(e)}]

    async def close(self) -> None:
        """Close the browser session."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


# Global session management
_session: Optional[PanoramaSession] = None


async def get_session(panorama_url: str, headless: bool = False) -> PanoramaSession:
    """Get or create a Panorama browser session."""
    global _session

    if _session is None or _session.panorama_url != panorama_url:
        if _session:
            await _session.close()
        _session = PanoramaSession(panorama_url=panorama_url)
        await _session.initialize(headless=headless)

    return _session


async def close_session() -> None:
    """Close the current session."""
    global _session
    if _session:
        await _session.close()
        _session = None
