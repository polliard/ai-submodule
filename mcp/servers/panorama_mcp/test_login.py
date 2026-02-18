#!/usr/bin/env python3
"""
Simple SSO login test - keeps browser open for login.
"""

import asyncio
import sys
from playwright.async_api import async_playwright

PANORAMA_URL = "https://panoramav2.corp.jmfamily.com"


async def main():
    print("=" * 60)
    print("Panorama SSO Login Test")
    print("=" * 60)
    print(f"\nOpening: {PANORAMA_URL}")
    print("\n>>> Complete your SSO login in the browser <<<")
    print(">>> Press Ctrl+C in terminal when done to save session <<<\n")

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # Navigate to Panorama
    await page.goto(PANORAMA_URL, wait_until="networkidle")
    print(f"Current page: {page.url}")

    try:
        # Keep checking until user presses Ctrl+C
        while True:
            await asyncio.sleep(3)
            try:
                # Wait for any navigation to complete
                await page.wait_for_load_state("domcontentloaded", timeout=2000)
                url = page.url
                print(f"Current URL: {url}")

                # Check if we're past login screens (Panorama app uses hash routing)
                if "panoramav2" in url and "#" in url:
                    print("\n✓ Appears to be logged in! (on Panorama app)")
                    print("Press Ctrl+C to save session and exit.")
            except Exception:
                print("Page navigating... waiting")

    except KeyboardInterrupt:
        print("\n\nSaving session state...")

        # Save auth state
        import os
        from pathlib import Path
        storage_path = Path.home() / ".panorama_mcp" / "auth_state.json"
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        await context.storage_state(path=str(storage_path))
        print(f"✓ Session saved to: {storage_path}")

    finally:
        await browser.close()
        await playwright.stop()
        print("Browser closed.")


if __name__ == "__main__":
    asyncio.run(main())
