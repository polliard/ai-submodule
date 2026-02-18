"""
Panorama-specific page scrapers for policy management and log monitoring.
"""

import asyncio
import re
from typing import Any, Optional
from .browser import PanoramaSession, get_session


class PanoramaScraper:
    """Scraper for Panorama web interface."""

    def __init__(self, session: PanoramaSession):
        self.session = session

    async def navigate_to_policies(self, device_group: str = "shared") -> dict:
        """Navigate to the Policies section."""
        if not self.session.page:
            return {"error": "Browser not initialized"}

        try:
            # Panorama navigation structure
            base_url = self.session.panorama_url.rstrip('/')
            policies_url = f"{base_url}/#policies/security"

            await self.session.page.goto(policies_url, wait_until="networkidle")

            # Wait for policy table to load
            await self.session.page.wait_for_selector('.grid-body, .policy-table, table', timeout=15000)

            return {
                "success": True,
                "url": self.session.page.url,
                "device_group": device_group
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_security_policies(self, device_group: str = "shared") -> list[dict]:
        """Get security policies for a device group."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            # Navigate to policies if not already there
            await self.navigate_to_policies(device_group)

            # Wait for the policy grid to load
            await asyncio.sleep(2)  # Allow JS to populate

            # Try to extract policy data from the grid
            policies = await self.session.page.evaluate("""
                () => {
                    const policies = [];

                    // Try common Panorama grid selectors
                    const rows = document.querySelectorAll('.grid-row, .policy-row, tbody tr');

                    rows.forEach((row, index) => {
                        const cells = row.querySelectorAll('.grid-cell, td');
                        if (cells.length > 0) {
                            const policy = {
                                index: index,
                                name: '',
                                source: '',
                                destination: '',
                                application: '',
                                service: '',
                                action: ''
                            };

                            // Try to extract text content from cells
                            if (cells[0]) policy.name = cells[0].textContent?.trim() || '';
                            if (cells[1]) policy.source = cells[1].textContent?.trim() || '';
                            if (cells[2]) policy.destination = cells[2].textContent?.trim() || '';
                            if (cells[3]) policy.application = cells[3].textContent?.trim() || '';
                            if (cells[4]) policy.service = cells[4].textContent?.trim() || '';
                            if (cells[5]) policy.action = cells[5].textContent?.trim() || '';

                            if (policy.name) {
                                policies.push(policy);
                            }
                        }
                    });

                    return policies;
                }
            """)

            return policies if policies else [{"message": "No policies found or unable to parse grid"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def get_nat_policies(self, device_group: str = "shared") -> list[dict]:
        """Get NAT policies for a device group."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            base_url = self.session.panorama_url.rstrip('/')
            nat_url = f"{base_url}/#policies/nat"

            await self.session.page.goto(nat_url, wait_until="networkidle")
            await asyncio.sleep(2)

            nat_policies = await self.session.page.evaluate("""
                () => {
                    const policies = [];
                    const rows = document.querySelectorAll('.grid-row, .nat-row, tbody tr');

                    rows.forEach((row, index) => {
                        const cells = row.querySelectorAll('.grid-cell, td');
                        if (cells.length > 0) {
                            const policy = {
                                index: index,
                                name: cells[0]?.textContent?.trim() || '',
                                source_zone: cells[1]?.textContent?.trim() || '',
                                destination_zone: cells[2]?.textContent?.trim() || '',
                                source_address: cells[3]?.textContent?.trim() || '',
                                destination_address: cells[4]?.textContent?.trim() || '',
                                translated_address: cells[5]?.textContent?.trim() || ''
                            };
                            if (policy.name) policies.push(policy);
                        }
                    });

                    return policies;
                }
            """)

            return nat_policies if nat_policies else [{"message": "No NAT policies found"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def navigate_to_monitor(self, log_type: str = "traffic") -> dict:
        """Navigate to Monitor > Logs section."""
        if not self.session.page:
            return {"error": "Browser not initialized"}

        try:
            base_url = self.session.panorama_url.rstrip('/')
            monitor_url = f"{base_url}/#monitor/logs/{log_type}"

            await self.session.page.goto(monitor_url, wait_until="networkidle")

            # Wait for log viewer to load
            await self.session.page.wait_for_selector('.log-viewer, .grid-body, table', timeout=15000)

            return {
                "success": True,
                "url": self.session.page.url,
                "log_type": log_type
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_traffic_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get traffic logs with optional filter query."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            await self.navigate_to_monitor("traffic")

            # If query provided, enter it in the filter
            if query:
                filter_input = await self.session.page.query_selector('input[placeholder*="filter"], .filter-input, #logFilter')
                if filter_input:
                    await filter_input.fill(query)
                    await self.session.page.keyboard.press('Enter')
                    await asyncio.sleep(3)  # Wait for filter to apply

            await asyncio.sleep(2)

            logs = await self.session.page.evaluate(f"""
                () => {{
                    const logs = [];
                    const rows = document.querySelectorAll('.log-row, .grid-row, tbody tr');

                    const limit = {limit};
                    let count = 0;

                    rows.forEach((row) => {{
                        if (count >= limit) return;

                        const cells = row.querySelectorAll('.grid-cell, td');
                        if (cells.length > 0) {{
                            const log = {{
                                receive_time: cells[0]?.textContent?.trim() || '',
                                type: cells[1]?.textContent?.trim() || '',
                                source_ip: cells[2]?.textContent?.trim() || '',
                                destination_ip: cells[3]?.textContent?.trim() || '',
                                application: cells[4]?.textContent?.trim() || '',
                                action: cells[5]?.textContent?.trim() || '',
                                rule: cells[6]?.textContent?.trim() || ''
                            }};
                            if (log.source_ip || log.receive_time) {{
                                logs.push(log);
                                count++;
                            }}
                        }}
                    }});

                    return logs;
                }}
            """)

            return logs if logs else [{"message": "No traffic logs found"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def get_threat_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get threat logs with optional filter query."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            await self.navigate_to_monitor("threat")

            if query:
                filter_input = await self.session.page.query_selector('input[placeholder*="filter"], .filter-input')
                if filter_input:
                    await filter_input.fill(query)
                    await self.session.page.keyboard.press('Enter')
                    await asyncio.sleep(3)

            await asyncio.sleep(2)

            logs = await self.session.page.evaluate(f"""
                () => {{
                    const logs = [];
                    const rows = document.querySelectorAll('.log-row, .grid-row, tbody tr');

                    const limit = {limit};
                    let count = 0;

                    rows.forEach((row) => {{
                        if (count >= limit) return;

                        const cells = row.querySelectorAll('.grid-cell, td');
                        if (cells.length > 0) {{
                            const log = {{
                                receive_time: cells[0]?.textContent?.trim() || '',
                                threat_name: cells[1]?.textContent?.trim() || '',
                                threat_id: cells[2]?.textContent?.trim() || '',
                                source_ip: cells[3]?.textContent?.trim() || '',
                                destination_ip: cells[4]?.textContent?.trim() || '',
                                severity: cells[5]?.textContent?.trim() || '',
                                action: cells[6]?.textContent?.trim() || ''
                            }};
                            if (log.threat_name || log.receive_time) {{
                                logs.push(log);
                                count++;
                            }}
                        }}
                    }});

                    return logs;
                }}
            """)

            return logs if logs else [{"message": "No threat logs found"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def get_system_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get system logs."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            await self.navigate_to_monitor("system")

            if query:
                filter_input = await self.session.page.query_selector('input[placeholder*="filter"], .filter-input')
                if filter_input:
                    await filter_input.fill(query)
                    await self.session.page.keyboard.press('Enter')
                    await asyncio.sleep(3)

            await asyncio.sleep(2)

            logs = await self.session.page.evaluate(f"""
                () => {{
                    const logs = [];
                    const rows = document.querySelectorAll('.log-row, .grid-row, tbody tr');

                    const limit = {limit};
                    let count = 0;

                    rows.forEach((row) => {{
                        if (count >= limit) return;

                        const cells = row.querySelectorAll('.grid-cell, td');
                        if (cells.length > 0) {{
                            const log = {{
                                receive_time: cells[0]?.textContent?.trim() || '',
                                serial: cells[1]?.textContent?.trim() || '',
                                type: cells[2]?.textContent?.trim() || '',
                                subtype: cells[3]?.textContent?.trim() || '',
                                description: cells[4]?.textContent?.trim() || ''
                            }};
                            if (log.description || log.receive_time) {{
                                logs.push(log);
                                count++;
                            }}
                        }}
                    }});

                    return logs;
                }}
            """)

            return logs if logs else [{"message": "No system logs found"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def get_device_groups(self) -> list[dict]:
        """Get list of device groups."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            base_url = self.session.panorama_url.rstrip('/')
            await self.session.page.goto(f"{base_url}/#panorama/device_groups", wait_until="networkidle")
            await asyncio.sleep(2)

            device_groups = await self.session.page.evaluate("""
                () => {
                    const groups = [];
                    const items = document.querySelectorAll('.device-group-item, .tree-node, .grid-row, li');

                    items.forEach(item => {
                        const name = item.textContent?.trim();
                        if (name && !name.includes('\\n')) {
                            groups.push({ name: name });
                        }
                    });

                    return groups;
                }
            """)

            return device_groups if device_groups else [{"message": "No device groups found"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def get_managed_devices(self) -> list[dict]:
        """Get list of managed firewalls."""
        if not self.session.page:
            return [{"error": "Browser not initialized"}]

        try:
            base_url = self.session.panorama_url.rstrip('/')
            await self.session.page.goto(f"{base_url}/#panorama/managed_devices", wait_until="networkidle")
            await asyncio.sleep(2)

            devices = await self.session.page.evaluate("""
                () => {
                    const devices = [];
                    const rows = document.querySelectorAll('.device-row, .grid-row, tbody tr');

                    rows.forEach(row => {
                        const cells = row.querySelectorAll('.grid-cell, td');
                        if (cells.length > 0) {
                            const device = {
                                name: cells[0]?.textContent?.trim() || '',
                                serial: cells[1]?.textContent?.trim() || '',
                                ip_address: cells[2]?.textContent?.trim() || '',
                                model: cells[3]?.textContent?.trim() || '',
                                sw_version: cells[4]?.textContent?.trim() || '',
                                status: cells[5]?.textContent?.trim() || ''
                            };
                            if (device.name || device.serial) {
                                devices.push(device);
                            }
                        }
                    });

                    return devices;
                }
            """)

            return devices if devices else [{"message": "No managed devices found"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def commit_changes(self, device_group: Optional[str] = None) -> dict:
        """Trigger a commit operation."""
        if not self.session.page:
            return {"error": "Browser not initialized"}

        try:
            # Click the Commit button
            commit_button = await self.session.page.query_selector('button:has-text("Commit"), .commit-button, #commitBtn')

            if commit_button:
                await commit_button.click()
                await asyncio.sleep(2)

                # Look for commit dialog
                commit_dialog = await self.session.page.query_selector('.commit-dialog, .modal, dialog')

                if device_group and commit_dialog:
                    # Select device group if specified
                    dg_selector = await self.session.page.query_selector(f'option:has-text("{device_group}"), input[value="{device_group}"]')
                    if dg_selector:
                        await dg_selector.click()

                # Click confirm/OK
                confirm_button = await self.session.page.query_selector('button:has-text("OK"), button:has-text("Commit"), .btn-primary')
                if confirm_button:
                    await confirm_button.click()
                    await asyncio.sleep(2)

                return {
                    "success": True,
                    "message": "Commit initiated",
                    "device_group": device_group
                }
            else:
                return {"success": False, "error": "Commit button not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def push_to_devices(self, device_group: str) -> dict:
        """Push configuration to devices in a device group."""
        if not self.session.page:
            return {"error": "Browser not initialized"}

        try:
            # Look for Push to Devices button
            push_button = await self.session.page.query_selector('button:has-text("Push to Devices"), .push-button')

            if push_button:
                await push_button.click()
                await asyncio.sleep(2)

                # Select device group
                dg_selector = await self.session.page.query_selector(f'label:has-text("{device_group}")')
                if dg_selector:
                    await dg_selector.click()

                # Confirm push
                confirm_button = await self.session.page.query_selector('button:has-text("OK"), button:has-text("Push")')
                if confirm_button:
                    await confirm_button.click()
                    await asyncio.sleep(2)

                return {
                    "success": True,
                    "message": f"Push initiated for device group: {device_group}"
                }
            else:
                return {"success": False, "error": "Push to Devices button not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
