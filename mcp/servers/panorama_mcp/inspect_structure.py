#!/usr/bin/env python3
"""
Capture Panorama page structure for selector tuning.
"""

import asyncio
import json
import os

os.environ["PANORAMA_URL"] = "https://panoramav2.corp.jmfamily.com"

from panorama_mcp.browser import get_session, close_session


async def main():
    print("Capturing Panorama page structure...")

    session = await get_session(os.environ["PANORAMA_URL"], headless=False)

    # Navigate to different pages and capture structure
    pages_to_check = [
        ("Dashboard", ""),
        ("Device Groups", "#panorama/device_groups"),
        ("Managed Devices", "#panorama/managed_devices"),
        ("Security Policies", "#policies/security"),
    ]

    for name, path in pages_to_check:
        print(f"\n{'='*60}")
        print(f"Page: {name}")
        print('='*60)

        url = f"{os.environ['PANORAMA_URL']}/{path}"
        await session.page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        # Get the HTML of key areas
        html_sample = await session.page.evaluate("""
            () => {
                // Get tables
                const tables = document.querySelectorAll('table');
                const tableInfo = Array.from(tables).slice(0, 3).map(t => ({
                    id: t.id || 'no-id',
                    class: t.className,
                    rows: t.querySelectorAll('tr').length
                }));

                // Get grids
                const grids = document.querySelectorAll('[class*="grid"], [class*="Grid"]');
                const gridInfo = Array.from(grids).slice(0, 5).map(g => ({
                    tag: g.tagName,
                    class: g.className,
                    children: g.children.length
                }));

                // Get any data containers
                const containers = document.querySelectorAll('[class*="content"], [class*="body"], [class*="panel"]');
                const containerInfo = Array.from(containers).slice(0, 5).map(c => ({
                    tag: c.tagName,
                    class: c.className.slice(0, 100)
                }));

                return {
                    tables: tableInfo,
                    grids: gridInfo,
                    containers: containerInfo,
                    url: window.location.href
                };
            }
        """)

        print(f"URL: {html_sample.get('url', 'N/A')}")
        print(f"\nTables found: {len(html_sample.get('tables', []))}")
        for t in html_sample.get('tables', []):
            print(f"  - id={t['id']}, class={t['class'][:50]}, rows={t['rows']}")

        print(f"\nGrids found: {len(html_sample.get('grids', []))}")
        for g in html_sample.get('grids', []):
            print(f"  - {g['tag']}, class={g['class'][:50]}, children={g['children']}")

        # Take screenshot
        safe_name = name.lower().replace(' ', '_')
        await session.page.screenshot(path=f"panorama_{safe_name}.png")
        print(f"\n✓ Screenshot: panorama_{safe_name}.png")

    print("\n\nDone! Check screenshots and output above to identify correct selectors.")
    input("\nPress Enter to close browser...")
    await close_session()


if __name__ == "__main__":
    asyncio.run(main())
