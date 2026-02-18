#!/usr/bin/env python3
"""
Interactive Panorama browser - keeps session alive for testing.
Login once, then run commands interactively.
"""

import asyncio
import os
import json

os.environ["PANORAMA_URL"] = "https://panoramav2.corp.jmfamily.com"

from playwright.async_api import async_playwright


class PanoramaBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.base_url = os.environ["PANORAMA_URL"]

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )
        self.page = await self.context.new_page()
        await self.page.goto(self.base_url, wait_until="domcontentloaded")
        print(f"Browser started at: {self.page.url}")

    async def wait_for_login(self):
        """Wait until user completes login."""
        print("\n>>> Complete SSO login in browser <<<")
        print(">>> Type 'done' when logged in <<<\n")

        while True:
            cmd = input("> ").strip().lower()
            if cmd == "done":
                if "/php/login.php" not in self.page.url:
                    print("✓ Login confirmed!")
                    return True
                else:
                    print("Still on login page...")
            elif cmd == "url":
                print(f"Current: {self.page.url}")
            elif cmd == "quit":
                return False

    async def navigate(self, section):
        """Navigate to a Panorama section."""
        sections = {
            "dashboard": "",
            "devices": "#panorama/managed_devices",
            "groups": "#panorama/device_groups",
            "security": "#policies/security",
            "nat": "#policies/nat",
            "traffic": "#monitor/logs/traffic",
            "threat": "#monitor/logs/threat",
            "system": "#monitor/logs/system",
        }

        if section in sections:
            url = f"{self.base_url}/{sections[section]}"
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            print(f"Navigated to: {self.page.url}")
        else:
            print(f"Unknown section. Available: {', '.join(sections.keys())}")

    async def screenshot(self, filename="panorama_screenshot.png"):
        await self.page.screenshot(path=filename)
        print(f"Screenshot saved: {filename}")

    async def get_page_text(self):
        """Get visible text from the page."""
        text = await self.page.evaluate("""
            () => {
                return document.body.innerText;
            }
        """)
        return text

    async def find_tables(self):
        """Find and describe tables on the page."""
        tables = await self.page.evaluate("""
            () => {
                const results = [];
                document.querySelectorAll('table').forEach((table, idx) => {
                    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
                    const rowCount = table.querySelectorAll('tbody tr').length;
                    results.push({
                        index: idx,
                        id: table.id || 'none',
                        className: table.className || 'none',
                        headers: headers.slice(0, 10),
                        rowCount: rowCount
                    });
                });
                return results;
            }
        """)
        return tables

    async def get_table_data(self, table_index=0):
        """Extract data from a specific table."""
        data = await self.page.evaluate(f"""
            () => {{
                const tables = document.querySelectorAll('table');
                if (tables.length <= {table_index}) return null;

                const table = tables[{table_index}];
                const headers = Array.from(table.querySelectorAll('thead th, tr:first-child th')).map(th => th.textContent.trim());
                const rows = [];

                table.querySelectorAll('tbody tr').forEach(tr => {{
                    const cells = Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
                    if (cells.length > 0) rows.push(cells);
                }});

                return {{ headers, rows: rows.slice(0, 20) }};
            }}
        """)
        return data

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser closed.")


async def main():
    print("=" * 60)
    print("Panorama Interactive Browser")
    print("=" * 60)

    browser = PanoramaBrowser()
    await browser.start()

    if not await browser.wait_for_login():
        await browser.close()
        return

    print("\nCommands:")
    print("  nav <section>  - Navigate (dashboard/devices/groups/security/nat/traffic/threat/system)")
    print("  tables         - List tables on current page")
    print("  data <idx>     - Get data from table at index")
    print("  text           - Show page text")
    print("  shot           - Take screenshot")
    print("  url            - Show current URL")
    print("  quit           - Exit")
    print()

    while True:
        try:
            cmd = input("panorama> ").strip()
            if not cmd:
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if action == "quit":
                break
            elif action == "nav":
                await browser.navigate(arg)
            elif action == "tables":
                tables = await browser.find_tables()
                print(f"Found {len(tables)} tables:")
                for t in tables:
                    print(f"  [{t['index']}] id={t['id']}, rows={t['rowCount']}, headers={t['headers'][:5]}")
            elif action == "data":
                idx = int(arg) if arg else 0
                data = await browser.get_table_data(idx)
                if data:
                    print(f"Headers: {data['headers']}")
                    print(f"Rows ({len(data['rows'])}):")
                    for row in data['rows'][:10]:
                        print(f"  {row}")
                else:
                    print("Table not found")
            elif action == "text":
                text = await browser.get_page_text()
                print(text[:2000])
            elif action == "shot":
                name = arg if arg else "panorama_screenshot.png"
                await browser.screenshot(name)
            elif action == "url":
                print(f"Current: {browser.page.url}")
            else:
                print(f"Unknown command: {action}")

        except KeyboardInterrupt:
            print("\nUse 'quit' to exit")
        except Exception as e:
            print(f"Error: {e}")

    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
