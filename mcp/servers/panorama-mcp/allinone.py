#!/usr/bin/env python3
"""
All-in-one Panorama MCP test - login and explore in single session.
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

PANORAMA_URL = "https://panoramav2.corp.jmfamily.com"


async def wait_for_login(page):
    """Wait for user to complete SSO login."""
    print("\n>>> Complete your SSO login in the browser <<<")
    print(">>> Script will auto-detect when logged in <<<\n")

    while True:
        await asyncio.sleep(2)
        try:
            current_url = page.url
            content = await page.content()

            # Check if logged in (not on login page, no session expired message)
            if "panoramav2.corp.jmfamily.com" in current_url:
                if "/php/login.php" not in current_url and "session has expired" not in content.lower():
                    print(f"✓ Login detected! URL: {current_url}")
                    return True
                elif "#" in current_url:
                    print(f"✓ Login detected! URL: {current_url}")
                    return True
        except:
            pass


async def explore_page(page, scraper_func, name):
    """Run a scraper function and display results."""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print('='*50)
    try:
        result = await scraper_func()
        if isinstance(result, list):
            print(f"Found {len(result)} items:")
            for i, item in enumerate(result[:10]):  # Show first 10
                print(f"  {i+1}. {item}")
        else:
            print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


async def main():
    print("=" * 60)
    print("Panorama MCP All-in-One Test")
    print("=" * 60)
    print(f"\nTarget: {PANORAMA_URL}")

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = await browser.new_context(
        viewport={'width': 1400, 'height': 900},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    )
    page = await context.new_page()

    try:
        # Navigate to Panorama
        print("\nNavigating to Panorama...")
        await page.goto(PANORAMA_URL, wait_until="domcontentloaded", timeout=30000)

        # Wait for login
        await wait_for_login(page)
        await asyncio.sleep(3)  # Let page stabilize

        # Save session
        storage_path = Path.home() / ".panorama_mcp" / "auth_state.json"
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        await context.storage_state(path=str(storage_path))
        print(f"✓ Session saved to: {storage_path}")

        # Interactive menu
        while True:
            print("\n" + "=" * 60)
            print("What would you like to explore?")
            print("=" * 60)
            print("1. Get page structure (accessibility tree)")
            print("2. Navigate to Policies > Security")
            print("3. Navigate to Monitor > Traffic Logs")
            print("4. Navigate to Panorama > Managed Devices")
            print("5. Navigate to Panorama > Device Groups")
            print("6. Take screenshot")
            print("7. Show current URL and page info")
            print("8. Enter custom URL path (e.g., #policies/security)")
            print("9. Extract table data from current page")
            print("0. Exit")
            print("-" * 60)

            choice = input("Enter choice: ").strip()

            if choice == "0":
                break
            elif choice == "1":
                print("\nGetting page structure...")
                snapshot = await page.accessibility.snapshot()
                if snapshot:
                    import json
                    # Save to file for analysis
                    with open("page_structure.json", "w") as f:
                        json.dump(snapshot, f, indent=2)
                    print("✓ Full structure saved to: page_structure.json")
                    # Show summary
                    def count_nodes(node):
                        count = 1
                        for child in node.get('children', []):
                            count += count_nodes(child)
                        return count
                    print(f"Total nodes: {count_nodes(snapshot)}")
                    print(f"Root: {snapshot.get('role')} - {snapshot.get('name', '')[:50]}")

            elif choice == "2":
                print("\nNavigating to Security Policies...")
                await page.goto(f"{PANORAMA_URL}/#policies/security", wait_until="networkidle", timeout=30000)
                print(f"Current URL: {page.url}")

            elif choice == "3":
                print("\nNavigating to Traffic Logs...")
                await page.goto(f"{PANORAMA_URL}/#monitor/logs/traffic", wait_until="networkidle", timeout=30000)
                print(f"Current URL: {page.url}")

            elif choice == "4":
                print("\nNavigating to Managed Devices...")
                await page.goto(f"{PANORAMA_URL}/#panorama/managed_devices", wait_until="networkidle", timeout=30000)
                print(f"Current URL: {page.url}")

            elif choice == "5":
                print("\nNavigating to Device Groups...")
                await page.goto(f"{PANORAMA_URL}/#panorama/device_groups", wait_until="networkidle", timeout=30000)
                print(f"Current URL: {page.url}")

            elif choice == "6":
                filename = f"panorama_screenshot_{int(asyncio.get_event_loop().time())}.png"
                await page.screenshot(path=filename)
                print(f"✓ Screenshot saved: {filename}")

            elif choice == "7":
                print(f"\nURL: {page.url}")
                print(f"Title: {await page.title()}")

            elif choice == "8":
                path = input("Enter path (e.g., #policies/nat): ").strip()
                if path:
                    full_url = f"{PANORAMA_URL}/{path}" if not path.startswith('#') else f"{PANORAMA_URL}/{path}"
                    print(f"Navigating to: {full_url}")
                    await page.goto(full_url, wait_until="networkidle", timeout=30000)
                    print(f"Current URL: {page.url}")

            elif choice == "9":
                print("\nLooking for tables on current page...")
                tables = await page.query_selector_all('table')
                print(f"Found {len(tables)} table elements")

                # Also look for grid-like structures
                grids = await page.query_selector_all('[role="grid"], .grid, .data-grid, .x-grid')
                print(f"Found {len(grids)} grid elements")

                # Try to extract any visible data
                all_rows = await page.query_selector_all('tr, [role="row"], .grid-row')
                print(f"Found {len(all_rows)} row-like elements")

                if all_rows:
                    print("\nFirst 5 rows content:")
                    for i, row in enumerate(all_rows[:5]):
                        text = await row.text_content()
                        if text:
                            print(f"  {i+1}. {text[:100]}...")
            else:
                print("Invalid choice")

    except KeyboardInterrupt:
        print("\n\nInterrupted")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await browser.close()
        await playwright.stop()
        print("\nBrowser closed.")


if __name__ == "__main__":
    asyncio.run(main())
