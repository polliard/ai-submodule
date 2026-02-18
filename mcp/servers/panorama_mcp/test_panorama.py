#!/usr/bin/env python3
"""
Test script for Panorama MCP Server.

Run with: source .venv/bin/activate && python test_panorama.py
"""

import asyncio
import os

# Set the Panorama URL
os.environ["PANORAMA_URL"] = "https://panoramav2.corp.jmfamily.com"
os.environ["PANORAMA_HEADLESS"] = "false"

from panorama_mcp.browser import get_session, close_session
from panorama_mcp.scraper import PanoramaScraper


async def main():
    print("=" * 60)
    print("Panorama MCP Server Test")
    print("=" * 60)
    print(f"\nConnecting to: {os.environ['PANORAMA_URL']}")
    print("\nInitializing browser session...")

    try:
        # Get session (will open browser)
        session = await get_session(
            os.environ["PANORAMA_URL"],
            headless=False
        )

        print("✓ Browser session initialized")

        # Check if already authenticated
        print("\nChecking authentication status...")
        is_auth = await session.check_login_status()

        if is_auth:
            print("✓ Already authenticated to Panorama!")

            # Create scraper and test some functions
            scraper = PanoramaScraper(session)

            print("\n--- Testing Device Groups ---")
            groups = await scraper.get_device_groups()
            print(f"Device groups found: {len(groups)}")
            for g in groups[:5]:  # Show first 5
                print(f"  - {g}")

            print("\n--- Testing Managed Devices ---")
            devices = await scraper.get_managed_devices()
            print(f"Managed devices found: {len(devices)}")
            for d in devices[:5]:  # Show first 5
                print(f"  - {d}")

            print("\n--- Testing Security Policies ---")
            policies = await scraper.get_security_policies()
            print(f"Security policies found: {len(policies)}")
            for p in policies[:3]:  # Show first 3
                print(f"  - {p}")

            print("\n--- Taking Screenshot ---")
            await session.take_screenshot("panorama_test_screenshot.png")
            print("✓ Screenshot saved to: panorama_test_screenshot.png")

        else:
            print("✗ Not authenticated. Starting SSO login...")
            print("\n>>> Please complete the SSO login in the browser window <<<")
            print(">>> Waiting up to 5 minutes for login... <<<\n")

            result = await session.wait_for_sso_login(timeout_seconds=300)
            print(f"\nLogin result: {result}")

        print("\n" + "=" * 60)
        print("Test complete!")
        print("=" * 60)

        # Keep browser open for inspection
        input("\nPress Enter to close browser...")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await close_session()
        print("\nBrowser session closed.")


if __name__ == "__main__":
    asyncio.run(main())
