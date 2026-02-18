#!/usr/bin/env python3
"""Explore Panorama internal API and grid extraction."""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from panorama_mcp.browser import PanoramaSession


async def main():
    url = "https://panoramav2.corp.jmfamily.com"
    s = PanoramaSession(panorama_url=url)
    await s.initialize(headless=False)
    try:
        await s.page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        if not await s._is_logged_in_on_current_page():
            await s._try_auto_sso(timeout=60)
            await asyncio.sleep(3)

        await s.dismiss_popups()
        print(f"Dashboard URL: {s.page.url}\n")

        # === PART 1: Try Panorama's internal PHP endpoints ===
        print("=== Trying Internal PHP Router ===")

        # The web UI uses DirectRouter for data
        php_result = await s.page.evaluate("""async () => {
            try {
                // Try the DirectRouter endpoint that Panorama ExtJS uses
                const resp = await fetch('/php/utils/router.php/PanDirect.run', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'PanDirect',
                        method: 'run',
                        data: ['PanoramaDeviceManagement.getManagedDevices', '{}'],
                        type: 'rpc',
                        tid: 1
                    })
                });
                const text = await resp.text();
                return {status: resp.status, body: text.substring(0, 3000)};
            } catch(e) {
                return {error: e.message};
            }
        }""")
        print(f"  DirectRouter: {json.dumps(php_result, indent=2)[:1500]}")

        # Try another common endpoint
        print("\n=== Trying config endpoint ===")
        config_result = await s.page.evaluate("""async () => {
            try {
                const resp = await fetch('/php/utils/router.php/PanDirect.run', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'PanDirect',
                        method: 'run',
                        data: ['DeviceGroup.getDeviceGroupNodes', '{}'],
                        type: 'rpc',
                        tid: 2
                    })
                });
                const text = await resp.text();
                return {status: resp.status, body: text.substring(0, 3000)};
            } catch(e) {
                return {error: e.message};
            }
        }""")
        print(f"  DeviceGroup: {json.dumps(config_result, indent=2)[:1500]}")

        # === PART 2: Intercept XHR to see what endpoints the UI uses ===
        print("\n=== Intercepting XHR requests ===")

        # Set up request interception
        requests_log = []
        async def log_request(request):
            if '/php/' in request.url or '/api/' in request.url:
                requests_log.append({
                    'url': request.url[:100],
                    'method': request.method,
                    'postData': (request.post_data or '')[:200]
                })

        s.page.on('request', log_request)

        # Click Panorama tab to trigger data fetching
        print("  Clicking Panorama tab and waiting for requests...")
        panorama_tab = await s.page.query_selector('text="Panorama"')
        await panorama_tab.click()
        await asyncio.sleep(8)  # Wait longer for data to load

        print(f"  Captured {len(requests_log)} API requests:")
        for req in requests_log[:20]:
            print(f"    {req['method']} {req['url']}")
            if req['postData']:
                print(f"      POST: {req['postData'][:150]}")

        s.page.remove_listener('request', log_request)

        # === PART 3: Try to extract grid data after longer wait ===
        print("\n=== Grid extraction (after longer wait) ===")

        # Try to get ALL visible text content in the main content area
        content = await s.page.evaluate("""() => {
            const result = {};

            // Find the main body/content panel
            const panels = document.querySelectorAll('[class*="x-panel-body"]');
            result.panelCount = panels.length;

            // Get text from the largest visible panel
            let maxPanel = null;
            let maxSize = 0;
            panels.forEach(p => {
                if (p.offsetParent && p.scrollHeight > maxSize) {
                    maxSize = p.scrollHeight;
                    maxPanel = p;
                }
            });

            if (maxPanel) {
                // Get all div/span text inside
                const texts = [];
                maxPanel.querySelectorAll('div, span, td').forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 2 && text.length < 60 &&
                        el.children.length === 0) {
                        texts.push(text);
                    }
                });
                result.mainPanelTexts = [...new Set(texts)].slice(0, 60);
            }

            // Try to find column headers
            const colHeaders = [];
            document.querySelectorAll('[class*="column-header"], [class*="grid-hd"]').forEach(h => {
                const text = h.textContent?.trim();
                if (text && text.length < 50) colHeaders.push(text);
            });
            result.columnHeaders = [...new Set(colHeaders)];

            return result;
        }""")

        print(f"  Panel count: {content.get('panelCount', 0)}")
        print(f"  Column headers: {content.get('columnHeaders', [])}")
        print(f"  Main panel texts ({len(content.get('mainPanelTexts', []))}):")
        for t in content.get('mainPanelTexts', [])[:30]:
            print(f"    {t}")

        # Take final screenshot
        await s.take_screenshot("/tmp/panorama_after_explore.png")
        print("\n  Screenshot: /tmp/panorama_after_explore.png")

    finally:
        await s.close()


asyncio.run(main())
