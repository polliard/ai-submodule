#!/usr/bin/env python3
"""
Fresh SSO login - clears all cookies/state first.
"""

import asyncio
import os
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright


def _parse_panorama_urls() -> list[str]:
    """Parse configured Panorama URLs from environment."""
    raw = os.environ.get("PANORAMA_URLS", "")
    if raw:
        return [u.strip().rstrip("/") for u in raw.split(",") if u.strip()]
    single = os.environ.get("PANORAMA_URL", "").strip().rstrip("/")
    if single:
        return [single]
    return ["https://panoramav2.corp.jmfamily.com"]


def _allowed_hosts(urls: list[str]) -> set[str]:
    """Build the set of valid hostnames from configured URLs."""
    return {urlparse(u).hostname for u in urls if urlparse(u).hostname}


def _is_allowed_url(url: str, hosts: set[str]) -> bool:
    """Validate that *url*'s hostname is in the allowed set."""
    try:
        return urlparse(url).hostname in hosts
    except Exception:
        return False


PANORAMA_URLS = _parse_panorama_urls()
PANORAMA_URL = PANORAMA_URLS[0]
ALLOWED_HOSTS = _allowed_hosts(PANORAMA_URLS)


async def main():
    print("=" * 60)
    print("Panorama Fresh SSO Login")
    print("=" * 60)

    # Clear any old auth state first
    storage_path = Path.home() / ".panorama_mcp" / "auth_state.json"
    if storage_path.exists():
        storage_path.unlink()
        print("✓ Cleared old session state")

    print(f"\nOpening: {PANORAMA_URL}")
    print("\n>>> Complete your SSO login in the browser <<<")
    print(">>> The script will auto-detect when you're logged in <<<\n")

    playwright = await async_playwright().start()

    # Launch with clean profile, no saved state
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']  # Less detectable
    )

    # Fresh context - no storage state
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 900},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    page = await context.new_page()

    # Go directly to the base URL (not login.php)
    print("Navigating to Panorama...")
    await page.goto(PANORAMA_URL, wait_until="domcontentloaded", timeout=30000)
    print(f"Initial URL: {page.url}")

    logged_in = False
    try:
        # Wait for user to complete login
        check_count = 0
        while not logged_in:
            await asyncio.sleep(2)
            check_count += 1

            try:
                current_url = page.url

                # Show progress every few checks
                if check_count % 5 == 0:
                    print(f"Waiting... Current: {current_url[:60]}...")

                # Detect successful login - Panorama uses hash routing when logged in
                if _is_allowed_url(current_url, ALLOWED_HOSTS):
                    # Check if we're past the login page
                    if "#" in current_url or "/php/login.php" not in current_url:
                        # Double check we're not on an error page
                        content = await page.content()
                        if "session has expired" not in content.lower():
                            print(f"\n✓ Login detected! URL: {current_url}")
                            logged_in = True
                            break

            except Exception as e:
                # Page might be navigating
                pass

        if logged_in:
            # Wait a moment for page to stabilize
            await asyncio.sleep(2)

            # Save the session
            print("\nSaving session state...")
            storage_path.parent.mkdir(parents=True, exist_ok=True)
            await context.storage_state(path=str(storage_path))
            print(f"✓ Session saved to: {storage_path}")

            # Take a screenshot as proof
            await page.screenshot(path="panorama_logged_in.png")
            print("✓ Screenshot saved: panorama_logged_in.png")

            input("\nPress Enter to close browser...")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        if not logged_in:
            # Try to save anyway
            try:
                storage_path.parent.mkdir(parents=True, exist_ok=True)
                await context.storage_state(path=str(storage_path))
                print(f"Session state saved to: {storage_path}")
            except:
                pass

    finally:
        await browser.close()
        await playwright.stop()
        print("Browser closed.")


if __name__ == "__main__":
    asyncio.run(main())
