#!/usr/bin/env python3
"""
Validate Panorama MCP connectivity.

Tests SSO login and basic data collection against a real Panorama instance.
Uses a SINGLE browser session for both login and validation — Panorama uses
session-only cookies that are destroyed when the browser closes.

Usage:
    python validate.py [PANORAMA_URL]

    Defaults to PANORAMA_URLS / PANORAMA_URL env var if no argument given.
    Default: https://panoramav2.corp.jmfamily.com
"""

import asyncio
import os
import sys

# Add parent to path so we can import the package directly
sys.path.insert(0, os.path.dirname(__file__))

from panorama_mcp.browser import PanoramaSession
from panorama_mcp.scraper import PanoramaScraper


DEFAULT_URL = "https://panoramav2.corp.jmfamily.com"


def _resolve_url() -> str:
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            url = arg.strip().rstrip("/")
            if not url.startswith("http"):
                url = f"https://{url}"
            return url

    env_urls = os.environ.get("PANORAMA_URLS", "")
    if env_urls:
        return env_urls.split(",")[0].strip().rstrip("/")

    env_url = os.environ.get("PANORAMA_URL", "").strip().rstrip("/")
    if env_url:
        return env_url

    return DEFAULT_URL


def _check(results: list, name: str, passed: bool, detail: str = ""):
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    results.append({"name": name, "passed": passed, "detail": detail})


async def validate(url: str) -> list:
    """Run full validation in a single browser session."""
    results: list = []

    # ---- Step 1: Launch visible browser ----
    session = PanoramaSession(panorama_url=url)
    try:
        await session.initialize(headless=False)
        _check(results, "Browser launch", True)
    except Exception as e:
        _check(results, "Browser launch", False, str(e))
        return results

    try:
        # ---- Step 2: Navigate and check auth ----
        await session.page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        logged_in = await session._is_logged_in_on_current_page()

        if not logged_in:
            _check(results, "Saved session", False, "session expired or missing")

            # ---- Step 3: Auto-SSO flow ----
            print("\n  Starting SSO authentication flow...\n")
            sso_result = await session._try_auto_sso(timeout=60)

            if not sso_result:
                # Auto-SSO didn't complete (IDP needs interaction)
                # Wait for user to complete MFA in the visible browser
                print(f"\n  {'='*56}")
                print("  Complete SSO login in the browser window.")
                print("  Once you see the Panorama dashboard, press ENTER here.")
                print("  (Ctrl+C to cancel)")
                print(f"  {'='*56}\n")

                # Use asyncio-friendly input
                loop = asyncio.get_event_loop()
                try:
                    await loop.run_in_executor(
                        None, input, "  Press ENTER when login is complete... "
                    )
                except KeyboardInterrupt:
                    print("\n  Cancelled.")
                    return results

                await asyncio.sleep(2)

                # Re-check auth after user interaction
                logged_in = await session._is_logged_in_on_current_page()
                if not logged_in:
                    # Try navigating back to Panorama (might have landed on IDP)
                    await session.page.goto(url, wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(3)
                    logged_in = await session._is_logged_in_on_current_page()

                _check(results, "SSO login", logged_in,
                       "authenticated" if logged_in else "still not authenticated")
            else:
                _check(results, "SSO login (auto)", True, "IDP session reused")
                logged_in = True
        else:
            _check(results, "Saved session", True, "authenticated from profile")

        if not logged_in:
            # Diagnostics
            diag_url = session.page.url if session.page else "unknown"
            print(f"\n  Diagnostics:")
            print(f"    Final URL: {diag_url}")
            try:
                diag_path = "/tmp/panorama_validate_fail.png"
                await session.take_screenshot(diag_path)
                print(f"    Screenshot: {diag_path}")
            except Exception:
                pass
            print(f"\n  Cannot continue without authentication.\n")
            return results

        # ---- Step 4: Dismiss popups ----
        await session.dismiss_popups()

        # ---- Step 5: Dashboard accessible ----
        info = await session.get_page_info()
        has_url = bool(info.get("url"))
        _check(results, "Dashboard accessible", has_url, info.get("url", ""))

        # ---- Step 6: Scrape device groups ----
        scraper = PanoramaScraper(session)
        try:
            groups = await scraper.get_device_groups()
            has_groups = len(groups) > 0 and "error" not in groups[0]
            detail = f"{len(groups)} groups found" if has_groups else str(groups)
            _check(results, "Device groups query", has_groups, detail)
        except Exception as e:
            _check(results, "Device groups query", False, str(e))

        # ---- Step 7: Scrape managed devices ----
        try:
            devices = await scraper.get_managed_devices()
            has_devices = len(devices) > 0 and "error" not in devices[0]
            detail = f"{len(devices)} devices found" if has_devices else str(devices)
            _check(results, "Managed devices query", has_devices, detail)
        except Exception as e:
            _check(results, "Managed devices query", False, str(e))

        # ---- Step 8: Screenshot test ----
        try:
            screenshot = await session.take_screenshot()
            has_screenshot = len(screenshot) > 1000  # non-trivial image
            _check(results, "Screenshot capture", has_screenshot, f"{len(screenshot)} bytes")
        except Exception as e:
            _check(results, "Screenshot capture", False, str(e))

    finally:
        await session.close()

    return results


def main():
    from urllib.parse import urlparse

    url = _resolve_url()
    host = urlparse(url).hostname

    print(f"\n{'='*60}")
    print(f"  Panorama MCP Validation")
    print(f"  Instance: {host}")
    print(f"{'='*60}\n")

    results = asyncio.run(validate(url))

    # Summary
    passed = sum(1 for c in results if c["passed"])
    total = len(results)
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} checks passed")
    print(f"{'='*60}\n")

    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
