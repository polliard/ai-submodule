#!/usr/bin/env python3
"""
Comprehensive validation of all Panorama MCP tools against a live instance.

Authenticates via SSO, then exercises every read-only scraper method and
browser tool, reporting PASS / FAIL / WARN for each.  Write operations
(commit, push) are intentionally skipped.

Usage:
    python validate.py [PANORAMA_URL]

    Defaults to PANORAMA_URLS / PANORAMA_URL env var if no argument given.
    Default: https://panoramav2.corp.jmfamily.com

Exit codes:
    0  All checks passed (or only WARN / INFO)
    1  One or more checks failed
"""

import asyncio
import json
import os
import sys
import time
from typing import Any
from urllib.parse import urlparse

# Add parent to path so we can import the package directly
sys.path.insert(0, os.path.dirname(__file__))

from panorama_mcp.browser import PanoramaSession
from panorama_mcp.scraper import PanoramaScraper


DEFAULT_URL = "https://panoramav2.corp.jmfamily.com"

# ── Colour helpers (ANSI) ─────────────────────────────────────────────
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_DIM = "\033[2m"
_RESET = "\033[0m"
_BOLD = "\033[1m"


# ── Result tracking ───────────────────────────────────────────────────
class CheckResult:
    __slots__ = ("name", "status", "detail", "elapsed_ms")

    def __init__(self, name: str, status: str, detail: str = "", elapsed_ms: int = 0):
        self.name = name
        self.status = status          # PASS | FAIL | WARN | INFO | SKIP
        self.detail = detail
        self.elapsed_ms = elapsed_ms


def _status_colour(status: str) -> str:
    return {
        "PASS": _GREEN, "FAIL": _RED, "WARN": _YELLOW,
        "INFO": _CYAN, "SKIP": _DIM,
    }.get(status, "")


def _print_result(r: CheckResult) -> None:
    clr = _status_colour(r.status)
    timing = f"  {_DIM}({r.elapsed_ms}ms){_RESET}" if r.elapsed_ms else ""
    detail = f" -- {r.detail}" if r.detail else ""
    print(f"  [{clr}{r.status:4s}{_RESET}] {r.name}{detail}{timing}")


# ── URL resolution ────────────────────────────────────────────────────
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


# ── Helpers to classify results ───────────────────────────────────────
def _has_error(data: Any) -> bool:
    """True when the data is clearly an error / empty sentinel."""
    if data is None:
        return True
    if isinstance(data, dict):
        return "error" in data
    if isinstance(data, list):
        if len(data) == 0:
            return False  # empty list is not an error, just no data
        # Every element is an error dict
        return all(isinstance(e, dict) and "error" in e for e in data)
    return False


def _has_only_raw(data: Any) -> bool:
    """True when every entry is a raw fallback (method worked but parsing didn't)."""
    if isinstance(data, list):
        return all(isinstance(e, dict) and "raw" in e and len(e) == 1 for e in data)
    if isinstance(data, dict):
        return "raw" in data and len(data) == 1
    return False


def _summarise(data: Any, max_len: int = 120) -> str:
    """One-line summary of a result for the report."""
    if isinstance(data, list):
        if len(data) == 0:
            return "empty list (no entries)"
        first = data[0]
        if isinstance(first, dict):
            if "error" in first:
                return f"error: {first['error'][:max_len]}"
            if "raw" in first:
                return f"raw fallback ({len(data)} entries)"
            # Try to find a name-ish key
            for k in ("@name", "name", "devicename", "serial"):
                if k in first:
                    names = [str(e.get(k, "?")) for e in data[:3]]
                    more = f" ... +{len(data)-3}" if len(data) > 3 else ""
                    return f"{len(data)} entries [{', '.join(names)}{more}]"
        return f"{len(data)} entries"
    if isinstance(data, dict):
        if "error" in data:
            return f"error: {data['error'][:max_len]}"
        if "raw" in data:
            return "raw fallback"
        keys = list(data.keys())
        return f"dict with {len(keys)} keys: {', '.join(keys[:6])}"
    if isinstance(data, (str, int, float, bool)):
        return str(data)[:max_len]
    return str(type(data).__name__)


# ── Core runner ───────────────────────────────────────────────────────
async def _run_check(
    name: str,
    coro,
    *,
    allow_empty: bool = False,
    warn_on_error: bool = False,
) -> CheckResult:
    """Execute a coroutine and classify the result."""
    t0 = time.monotonic()
    try:
        data = await coro
        elapsed = int((time.monotonic() - t0) * 1000)
        detail = _summarise(data)

        if _has_error(data):
            status = "WARN" if warn_on_error else "FAIL"
            return CheckResult(name, status, detail, elapsed)

        if _has_only_raw(data):
            return CheckResult(name, "WARN", f"raw fallback -- {detail}", elapsed)

        # Empty but allowed (some environments have no NAT rules, etc.)
        if isinstance(data, (list, dict)) and len(data) == 0:
            if allow_empty:
                return CheckResult(name, "PASS", "empty (allowed)", elapsed)
            return CheckResult(name, "WARN", "returned empty", elapsed)

        return CheckResult(name, "PASS", detail, elapsed)

    except Exception as exc:
        elapsed = int((time.monotonic() - t0) * 1000)
        status = "WARN" if warn_on_error else "FAIL"
        return CheckResult(name, status, f"exception: {exc}", elapsed)


# ── Authentication ────────────────────────────────────────────────────
async def _authenticate(session: PanoramaSession, url: str, results: list[CheckResult]) -> bool:
    """Handle SSO auth, appending results.  Returns True if authenticated."""
    try:
        await session.initialize(headless=False)
        r = CheckResult("Browser launch", "PASS")
        results.append(r); _print_result(r)
    except Exception as e:
        r = CheckResult("Browser launch", "FAIL", str(e))
        results.append(r); _print_result(r)
        return False

    await session.page.goto(url, wait_until="networkidle", timeout=30000)
    # Brief pause for JS hash routing redirect
    await asyncio.sleep(2)

    logged_in = await session._is_logged_in_on_current_page()

    if not logged_in:
        r = CheckResult("Saved session", "INFO", "not detected -- starting SSO flow")
        results.append(r); _print_result(r)
        print()
        sso_ok = await session._try_auto_sso(timeout=60)

        if not sso_ok:
            print(f"\n  {'='*56}")
            print("  Complete SSO login in the browser window.")
            print("  Polling for login completion (up to 120s)...")
            print(f"  {'='*56}\n")

            # Try interactive input if available, otherwise poll
            interactive = sys.stdin.isatty()
            if interactive:
                loop = asyncio.get_event_loop()
                try:
                    await loop.run_in_executor(None, input, "  Press ENTER when login is complete... ")
                except (KeyboardInterrupt, EOFError):
                    pass
                await asyncio.sleep(2)
            else:
                # Non-interactive: poll for up to 120 seconds
                poll_deadline = asyncio.get_event_loop().time() + 120
                while asyncio.get_event_loop().time() < poll_deadline:
                    await asyncio.sleep(3)
                    try:
                        await session.page.wait_for_load_state("networkidle", timeout=5000)
                    except Exception:
                        pass
                    if await session._is_logged_in_on_current_page():
                        break
                    if session._is_on_idp_page():
                        print("    ... waiting on IDP page")
                        continue
                    print(f"    ... checking ({session.page.url[:60]})")

            logged_in = await session._is_logged_in_on_current_page()
            if not logged_in:
                await session.page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(3)
                logged_in = await session._is_logged_in_on_current_page()

            r = CheckResult(
                "SSO login", "PASS" if logged_in else "FAIL",
                "authenticated" if logged_in else "still not authenticated",
            )
            results.append(r); _print_result(r)
        else:
            r = CheckResult("SSO login (auto)", "PASS", "IDP session reused")
            results.append(r); _print_result(r)
            logged_in = True
    else:
        r = CheckResult("Saved session", "PASS", "dashboard detected")
        results.append(r); _print_result(r)

    if not logged_in:
        diag_url = session.page.url if session.page else "unknown"
        print(f"\n  Diagnostics:")
        print(f"    Final URL: {diag_url}")
        try:
            await session.take_screenshot("/tmp/panorama_validate_fail.png")
            print(f"    Screenshot: /tmp/panorama_validate_fail.png")
        except Exception:
            pass
        print(f"\n  Cannot continue without authentication.\n")

    return logged_in


# ══════════════════════════════════════════════════════════════════════
# Main validation
# ══════════════════════════════════════════════════════════════════════
async def validate(url: str) -> list[CheckResult]:
    results: list[CheckResult] = []
    session = PanoramaSession(panorama_url=url)

    try:
        # ── Phase 1: Authentication ───────────────────────────────
        if not await _authenticate(session, url, results):
            return results
        await session.dismiss_popups()

        scraper = PanoramaScraper(session)

        # ── Phase 2a: JS Runtime Probe ────────────────────────────
        # Inspect the Panorama JS runtime to understand available APIs
        section = "JS Runtime Probe"
        print(f"  {_BOLD}--- {section} ---{_RESET}")
        try:
            probe = await session.page.evaluate("""() => {
                const result = {};

                // 1. Check Panos.direct structure
                result.panos_direct_type = typeof Panos?.direct;
                result.panos_direct_keys = typeof Panos?.direct === 'object'
                    ? Object.keys(Panos.direct).slice(0, 50) : [];
                result.has_rpcMethods = !!(Panos?.direct?._rpcMethods);
                result.has_run = typeof Panos?.direct?.run;

                // 2. Check for *Direct globals on window
                const directGlobals = Object.keys(window).filter(k =>
                    k.endsWith('Direct') && typeof window[k] !== 'undefined'
                ).sort();
                result.window_direct_globals = directGlobals;

                // 3. Check for Pan* globals
                const panGlobals = Object.keys(window).filter(k =>
                    k.startsWith('Pan') && !k.startsWith('PanTransition')
                    && typeof window[k] !== 'undefined'
                ).sort().slice(0, 30);
                result.pan_globals = panGlobals;

                // 4. If Panos.direct has methods as properties, list them
                if (typeof Panos?.direct === 'object') {
                    const fnKeys = Object.keys(Panos.direct).filter(
                        k => typeof Panos.direct[k] === 'function'
                    );
                    result.panos_direct_functions = fnKeys.slice(0, 30);

                    // Check for nested objects that might hold methods
                    const objKeys = Object.keys(Panos.direct).filter(
                        k => typeof Panos.direct[k] === 'object'
                        && Panos.direct[k] !== null
                        && k !== '_rpcMethods'
                    );
                    result.panos_direct_objects = {};
                    for (const k of objKeys.slice(0, 20)) {
                        const inner = Panos.direct[k];
                        result.panos_direct_objects[k] = Object.keys(inner)
                            .filter(m => typeof inner[m] === 'function')
                            .slice(0, 10);
                    }
                }

                // 5. Try to find how the run method dispatches
                if (typeof Panos?.direct?.run === 'function') {
                    result.run_source_snippet = Panos.direct.run.toString().slice(0, 300);
                }

                return result;
            }""")

            # Print key findings
            direct_keys = probe.get("panos_direct_keys", [])
            direct_fns = probe.get("panos_direct_functions", [])
            window_directs = probe.get("window_direct_globals", [])
            nested = probe.get("panos_direct_objects", {})

            detail_parts = []
            if direct_keys:
                detail_parts.append(f"Panos.direct keys: {len(direct_keys)}")
            if direct_fns:
                detail_parts.append(f"functions: {', '.join(direct_fns[:5])}")
            if window_directs:
                detail_parts.append(f"window *Direct: {', '.join(window_directs[:5])}")
            if nested:
                detail_parts.append(f"nested objects: {', '.join(nested.keys())}")

            r = CheckResult("JS runtime probe", "PASS", "; ".join(detail_parts) or "no RPC structure found")
            results.append(r); _print_result(r)

            # Print detailed findings
            if window_directs:
                print(f"    Window *Direct globals: {', '.join(window_directs)}")
            if nested:
                for ns, methods in nested.items():
                    if methods:
                        print(f"    Panos.direct.{ns}: {', '.join(methods[:8])}")
            run_snippet = probe.get("run_source_snippet", "")
            if run_snippet:
                print(f"    Panos.direct.run: {run_snippet[:150]}...")

            # Save full probe to /tmp for debugging
            import json as _json
            with open("/tmp/panorama_probe.json", "w") as f:
                _json.dump(probe, f, indent=2)
            print(f"    Full probe saved to /tmp/panorama_probe.json")

        except Exception as e:
            r = CheckResult("JS runtime probe", "FAIL", str(e)[:200])
            results.append(r); _print_result(r)

        # ── Phase 2b: Discover a real device group for scoped queries
        print()
        dg_name = "shared"
        try:
            groups = await scraper.get_device_groups()
            if groups and isinstance(groups[0], dict) and "name" in groups[0]:
                dg_name = groups[0]["name"]
        except Exception:
            pass

        # ────────────────────────────────────────────────────────────
        # Phase 3: System / Dashboard
        # ────────────────────────────────────────────────────────────
        section = "System / Dashboard"
        print(f"  {_BOLD}--- {section} ---{_RESET}")

        r = await _run_check("get_system_info", scraper.get_system_info())
        results.append(r); _print_result(r)

        r = await _run_check("get_device_summary", scraper.get_device_summary())
        results.append(r); _print_result(r)

        r = await _run_check("get_system_resources", scraper.get_system_resources())
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 4: Device management
        # ────────────────────────────────────────────────────────────
        section = "Device Management"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        r = await _run_check("get_device_groups", scraper.get_device_groups())
        results.append(r); _print_result(r)

        r = await _run_check("get_managed_devices", scraper.get_managed_devices())
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 5: Configuration
        # ────────────────────────────────────────────────────────────
        section = "Configuration"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        r = await _run_check("get_templates", scraper.get_templates())
        results.append(r); _print_result(r)

        r = await _run_check("get_commit_history (limit=5)", scraper.get_commit_history(limit=5))
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 6: Policies (pre / post / both)
        # ────────────────────────────────────────────────────────────
        section = f"Policies (dg={dg_name})"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        for pos in ("pre", "post", "both"):
            r = await _run_check(
                f"get_security_policies position={pos}",
                scraper.get_security_policies(dg_name, position=pos),
                allow_empty=True, warn_on_error=True,
            )
            results.append(r); _print_result(r)

        for pos in ("pre", "post", "both"):
            r = await _run_check(
                f"get_nat_policies position={pos}",
                scraper.get_nat_policies(dg_name, position=pos),
                allow_empty=True, warn_on_error=True,
            )
            results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 7: Objects
        # ────────────────────────────────────────────────────────────
        section = f"Objects (dg={dg_name})"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        r = await _run_check(
            "get_address_objects",
            scraper.get_address_objects(dg_name),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_service_objects",
            scraper.get_service_objects(dg_name),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_address_groups",
            scraper.get_address_groups(dg_name),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_service_groups",
            scraper.get_service_groups(dg_name),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        # Also test with "shared" if it's different
        if dg_name != "shared":
            section_shared = "Objects (dg=shared)"
            print(f"\n  {_BOLD}--- {section_shared} ---{_RESET}")

            for method_name, method_fn in [
                ("get_address_objects (shared)", scraper.get_address_objects("shared")),
                ("get_service_objects (shared)", scraper.get_service_objects("shared")),
                ("get_address_groups (shared)", scraper.get_address_groups("shared")),
                ("get_service_groups (shared)", scraper.get_service_groups("shared")),
            ]:
                r = await _run_check(method_name, method_fn, allow_empty=True, warn_on_error=True)
                results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 8: Network
        # ────────────────────────────────────────────────────────────
        section = "Network"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        r = await _run_check(
            "get_security_zones",
            scraper.get_security_zones(),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_interfaces",
            scraper.get_interfaces(),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_routing",
            scraper.get_routing(),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 9: Logs (small limits for speed)
        # ────────────────────────────────────────────────────────────
        section = "Logs (limit=5)"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        log_checks = [
            ("get_traffic_logs", scraper.get_traffic_logs("", 5)),
            ("get_threat_logs",  scraper.get_threat_logs("", 5)),
            ("get_system_logs",  scraper.get_system_logs("", 5)),
            ("get_url_logs",     scraper.get_url_logs("", 5)),
            ("get_wildfire_logs", scraper.get_wildfire_logs("", 5)),
            ("get_config_logs",  scraper.get_config_logs("", 5)),
        ]
        for name, coro in log_checks:
            r = await _run_check(name, coro, allow_empty=True, warn_on_error=True)
            results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 10: Monitoring
        # ────────────────────────────────────────────────────────────
        section = "Monitoring"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        r = await _run_check(
            "get_jobs (limit=5)",
            scraper.get_jobs("", 5),
            allow_empty=True, warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_ha_status",
            scraper.get_ha_status(),
            warn_on_error=True,
        )
        results.append(r); _print_result(r)

        r = await _run_check(
            "get_software_info",
            scraper.get_software_info(),
            warn_on_error=True,
        )
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 11: Power tools
        # ────────────────────────────────────────────────────────────
        section = "Power Tools"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        # discover_methods -- list namespaces
        r = await _run_check(
            "discover_methods (all namespaces)",
            scraper.discover_methods(""),
        )
        results.append(r); _print_result(r)

        # discover_methods -- specific namespace
        r = await _run_check(
            "discover_methods (DashboardDirect)",
            scraper.discover_methods("DashboardDirect"),
        )
        results.append(r); _print_result(r)

        # run_direct -- call a known, safe read-only method
        r = await _run_check(
            "run_direct (DashboardDirect.getSystemInfo)",
            scraper.run_direct(
                "DashboardDirect.getSystemInfo",
                [{"isCmsSelected": True, "isMultiVsys": False, "getTestXML": False, "vsysName": ""}],
            ),
        )
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 12: Browser tools
        # ────────────────────────────────────────────────────────────
        section = "Browser Tools"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")

        # Screenshot
        t0 = time.monotonic()
        try:
            screenshot_bytes = await session.take_screenshot()
            elapsed = int((time.monotonic() - t0) * 1000)
            ok = len(screenshot_bytes) > 1000
            r = CheckResult(
                "take_screenshot",
                "PASS" if ok else "WARN",
                f"{len(screenshot_bytes)} bytes",
                elapsed,
            )
        except Exception as e:
            elapsed = int((time.monotonic() - t0) * 1000)
            r = CheckResult("take_screenshot", "FAIL", str(e), elapsed)
        results.append(r); _print_result(r)

        # Page info
        t0 = time.monotonic()
        try:
            page_info = await session.get_page_info()
            elapsed = int((time.monotonic() - t0) * 1000)
            ok = bool(page_info.get("url"))
            r = CheckResult(
                "get_page_info",
                "PASS" if ok else "WARN",
                page_info.get("url", "(no url)"),
                elapsed,
            )
        except Exception as e:
            elapsed = int((time.monotonic() - t0) * 1000)
            r = CheckResult("get_page_info", "FAIL", str(e), elapsed)
        results.append(r); _print_result(r)

        # Accessibility snapshot
        t0 = time.monotonic()
        try:
            snapshot = await session.get_page_snapshot()
            elapsed = int((time.monotonic() - t0) * 1000)
            ok = len(snapshot) > 10
            r = CheckResult(
                "get_page_snapshot",
                "PASS" if ok else "WARN",
                f"{len(snapshot)} chars",
                elapsed,
            )
        except Exception as e:
            elapsed = int((time.monotonic() - t0) * 1000)
            r = CheckResult("get_page_snapshot", "FAIL", str(e), elapsed)
        results.append(r); _print_result(r)

        # ────────────────────────────────────────────────────────────
        # Phase 13: Skipped write operations
        # ────────────────────────────────────────────────────────────
        section = "Write Operations (skipped -- read-only validation)"
        print(f"\n  {_BOLD}--- {section} ---{_RESET}")
        for op in ("commit_changes", "push_to_devices"):
            r = CheckResult(op, "SKIP", "write operation intentionally skipped")
            results.append(r); _print_result(r)

    finally:
        await session.close()

    return results


# ══════════════════════════════════════════════════════════════════════
# Report & entry point
# ══════════════════════════════════════════════════════════════════════
def _print_summary(results: list[CheckResult]) -> bool:
    """Print final summary table.  Returns True if no hard failures."""
    counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "INFO": 0, "SKIP": 0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1

    total = len(results)
    pass_count = counts["PASS"]
    fail_count = counts["FAIL"]
    warn_count = counts["WARN"]
    info_count = counts["INFO"]
    skip_count = counts["SKIP"]

    print(f"\n{'='*64}")
    print(f"  {_BOLD}Validation Summary{_RESET}")
    print(f"{'='*64}")
    print(f"  Total checks:  {total}")
    print(f"  {_GREEN}PASS:{_RESET}  {pass_count}")
    if fail_count:
        print(f"  {_RED}FAIL:{_RESET}  {fail_count}")
    if warn_count:
        print(f"  {_YELLOW}WARN:{_RESET}  {warn_count}")
    if info_count:
        print(f"  {_CYAN}INFO:{_RESET}  {info_count}")
    if skip_count:
        print(f"  {_DIM}SKIP:{_RESET}  {skip_count}")

    if fail_count:
        print(f"\n  {_RED}Failed checks:{_RESET}")
        for r in results:
            if r.status == "FAIL":
                print(f"    - {r.name}: {r.detail}")

    if warn_count:
        print(f"\n  {_YELLOW}Warnings (non-fatal):{_RESET}")
        for r in results:
            if r.status == "WARN":
                print(f"    - {r.name}: {r.detail}")

    print(f"{'='*64}\n")

    return fail_count == 0


def main():
    url = _resolve_url()
    host = urlparse(url).hostname

    print(f"\n{'='*64}")
    print(f"  {_BOLD}Panorama MCP -- Comprehensive Validation{_RESET}")
    print(f"  Instance: {host}")
    print(f"  Tools:    36 (testing all read-only tools)")
    print(f"{'='*64}\n")

    results = asyncio.run(validate(url))
    ok = _print_summary(results)

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
