#!/usr/bin/env python3
"""
Test Panorama MCP tools with saved session.
"""

import asyncio
import os

os.environ["PANORAMA_URL"] = "https://panoramav2.corp.jmfamily.com"
os.environ["PANORAMA_HEADLESS"] = "false"

from panorama_mcp.browser import get_session, close_session
from panorama_mcp.scraper import PanoramaScraper


async def main():
    print("=" * 60)
    print("Testing Panorama MCP Tools")
    print("=" * 60)

    session = await get_session(os.environ["PANORAMA_URL"], headless=False)
    scraper = PanoramaScraper(session)

    print("\n--- Getting Device Groups ---")
    try:
        groups = await scraper.get_device_groups()
        print(f"Found {len(groups)} device groups:")
        for g in groups[:10]:
            print(f"  • {g}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Getting Managed Devices ---")
    try:
        devices = await scraper.get_managed_devices()
        print(f"Found {len(devices)} devices:")
        for d in devices[:10]:
            print(f"  • {d}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Getting Security Policies ---")
    try:
        policies = await scraper.get_security_policies()
        print(f"Found {len(policies)} policies:")
        for p in policies[:5]:
            print(f"  • {p}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Taking Screenshot ---")
    try:
        await session.take_screenshot("panorama_test.png")
        print("✓ Screenshot saved: panorama_test.png")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 60)
    input("Press Enter to close browser...")
    await close_session()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
