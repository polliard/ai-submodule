"""
Panorama data access via the internal PanDirect RPC API.

Uses Panos.direct.run() in the browser context to call Panorama's internal
PHP endpoints.  This is the same mechanism the Panorama web UI uses and
handles CSRF tokens automatically.  It returns structured JSON, avoiding
fragile DOM scraping.
"""

import asyncio
import json
import logging
from typing import Any, Optional
from .browser import PanoramaSession

logger = logging.getLogger(__name__)


class PanoramaScraper:
    """Access Panorama data through the internal PanDirect API."""

    def __init__(self, session: PanoramaSession):
        self.session = session

    # ------------------------------------------------------------------
    # Core RPC helper
    # ------------------------------------------------------------------
    async def _run_direct(
        self,
        method: str,
        params: list | None = None,
        timeout: int = 30000,
    ) -> Any:
        """
        Call a Panorama PanDirect RPC method via the browser's JS context.

        The Panos.direct.run() function handles CSRF token generation and
        sends the request through the authenticated session.

        Returns the parsed result or raises on error.
        """
        if not self.session.page:
            raise RuntimeError("Browser not initialized")

        params_json = json.dumps(params or [])

        result = await self.session.page.evaluate(
            """([method, paramsJson, timeout]) => {
                return new Promise((resolve, reject) => {
                    const params = JSON.parse(paramsJson);
                    const timer = setTimeout(() => {
                        reject(new Error('Panos.direct.run timed out after ' + timeout + 'ms'));
                    }, timeout);

                    try {
                        Panos.direct.run(method, params, function(result, response) {
                            clearTimeout(timer);
                            if (!response.status) {
                                reject(new Error('RPC error: ' + JSON.stringify(result)));
                            } else {
                                resolve(result);
                            }
                        });
                    } catch(e) {
                        clearTimeout(timer);
                        reject(e);
                    }
                });
            }""",
            [method, params_json, timeout],
        )
        return result

    # ------------------------------------------------------------------
    # Config API helper (xpath-based queries)
    # ------------------------------------------------------------------
    async def _get_config(self, xpath: str) -> Any:
        """Query Panorama config API via the browser's authenticated session.

        Uses XMLHttpRequest to call /api/?type=config&action=get with the
        given xpath.  The browser's existing session cookies handle auth.
        """
        if not self.session.page:
            raise RuntimeError("Browser not initialized")

        result = await self.session.page.evaluate(
            """(xpath) => {
                return new Promise((resolve, reject) => {
                    const xhr = new XMLHttpRequest();
                    xhr.open('GET', '/api/?type=config&action=get&xpath=' + encodeURIComponent(xpath), true);
                    xhr.onload = () => {
                        try {
                            resolve({ status: xhr.status, text: xhr.responseText });
                        } catch(e) { reject(e); }
                    };
                    xhr.onerror = () => reject(new Error('Config API request failed'));
                    xhr.send();
                });
            }""", xpath)
        return result

    # ------------------------------------------------------------------
    # Multi-method fallback helper
    # ------------------------------------------------------------------
    async def _try_methods(
        self,
        methods: list[tuple[str, list]],
        timeout: int = 30000,
    ) -> tuple[Any, str | None]:
        """
        Try multiple PanDirect method/param combos, return first success.

        Returns (result, method_name) on success or (None, None) if all fail.
        """
        last_error = None
        for method_name, params in methods:
            try:
                result = await self._run_direct(method_name, params, timeout)
                return result, method_name
            except Exception as e:
                last_error = e
                logger.debug("_try_methods: %s failed: %s", method_name, e)
                continue
        return None, None

    # ------------------------------------------------------------------
    # System info
    # ------------------------------------------------------------------
    async def get_system_info(self) -> dict:
        """Get Panorama system information (hostname, IP, version, etc.)."""
        raw = await self._run_direct(
            "DashboardDirect.getSystemInfo",
            [{"isCmsSelected": True, "isMultiVsys": False, "getTestXML": False, "vsysName": ""}],
        )
        # Extract the nested system data
        try:
            return raw["result"]["data"]["system"]
        except (KeyError, TypeError):
            return raw

    # ------------------------------------------------------------------
    # Device groups
    # ------------------------------------------------------------------
    async def get_device_groups(self) -> list[dict]:
        """Get list of device groups with device counts."""
        raw = await self._run_direct(
            "DashboardDirect.getManagedDevicesInfo",
            [{"isCmsSelected": True, "isMultiVsys": False, "getTestXML": False, "vsysName": ""}],
        )
        try:
            entries = raw["result"]["data"]["device-summary"]["dg-summary"]["entry"]
            return [
                {"name": e["@name"], "device_count": int(e.get("count", 0))}
                for e in entries
            ]
        except (KeyError, TypeError):
            return [{"raw": raw}]

    # ------------------------------------------------------------------
    # Managed devices
    # ------------------------------------------------------------------
    async def get_managed_devices(self) -> list[dict]:
        """Get list of managed firewalls with full details."""
        raw = await self._run_direct(
            "DeviceDirect.getGroupedManagedDevices",
            [{"type": "all"}],
        )
        try:
            entries = raw["result"]["entry"]
            if isinstance(entries, dict):
                entries = [entries]
            devices = []
            for e in entries:
                devices.append({
                    "name": e.get("devicename", ""),
                    "serial": e.get("serial", ""),
                    "ip_address": e.get("ip-address", ""),
                    "model": e.get("model", ""),
                    "sw_version": e.get("sw-version", ""),
                    "connected": e.get("connected", ""),
                    "ha_mode": e.get("haMode", ""),
                    "device_group": e.get("device-group", ""),
                    "template": e.get("template", ""),
                    "operational_mode": e.get("operational-mode", ""),
                })
            return devices
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    # ------------------------------------------------------------------
    # Device summary
    # ------------------------------------------------------------------
    async def get_device_summary(self) -> dict:
        """Get managed device summary (counts, version distribution)."""
        raw = await self._run_direct(
            "DashboardDirect.getManagedDevicesInfo",
            [{"isCmsSelected": True, "isMultiVsys": False, "getTestXML": False, "vsysName": ""}],
        )
        try:
            summary = raw["result"]["data"]["device-summary"]
            result = {
                "connected": int(summary.get("connected", 0)),
                "disconnected": int(summary.get("dis-connected", 0)),
            }
            # Software version distribution
            if "sw-version" in summary and "entry" in summary["sw-version"]:
                result["sw_versions"] = [
                    {"version": e["@name"], "count": int(e["count"])}
                    for e in summary["sw-version"]["entry"]
                ]
            # Device group distribution
            if "dg-summary" in summary and "entry" in summary["dg-summary"]:
                result["device_groups"] = [
                    {"name": e["@name"], "count": int(e["count"])}
                    for e in summary["dg-summary"]["entry"]
                ]
            return result
        except (KeyError, TypeError):
            return {"raw": str(raw)[:500]}

    # ------------------------------------------------------------------
    # Policies (config API via PanDirect)
    # ------------------------------------------------------------------
    async def _get_policies(
        self, policy_type: str, device_group: str, position: str,
    ) -> list[dict]:
        """Fetch pre, post, or both rulebases for a given policy type."""
        positions = ["pre", "post"] if position == "both" else [position]
        all_entries: list[dict] = []
        for pos in positions:
            try:
                raw, method = await self._try_methods([
                    ("PoliciesDirect.getRules", [{"dg": device_group, "type": policy_type, "position": pos}]),
                    (f"PoliciesDirect.get{pos.capitalize()}Rules", [{"dg": device_group, "type": policy_type}]),
                ])
                if raw is None:
                    # Config API fallback via xpath
                    xpath = f"/config/devices/entry/device-group/entry[@name='{device_group}']/{pos}-rulebase/{policy_type}/rules"
                    try:
                        config_result = await self._get_config(xpath)
                        raw = config_result
                    except Exception:
                        all_entries.append({"error": "No working method found for policies", "position": pos})
                        continue
                entries = self._parse_policy_entries(raw)
                if position == "both":
                    for entry in entries:
                        if isinstance(entry, dict) and "error" not in entry and "raw" not in entry:
                            entry["_position"] = pos
                all_entries.extend(entries)
            except Exception as e:
                all_entries.append({"error": str(e), "position": pos})
        return all_entries

    async def get_security_policies(
        self, device_group: str = "shared", position: str = "both",
    ) -> list[dict]:
        """Get security policies for a device group.

        Args:
            device_group: Device group name.
            position: Rulebase position — "pre", "post", or "both" (default).
        """
        return await self._get_policies("security", device_group, position)

    async def get_nat_policies(
        self, device_group: str = "shared", position: str = "both",
    ) -> list[dict]:
        """Get NAT policies for a device group.

        Args:
            device_group: Device group name.
            position: Rulebase position — "pre", "post", or "both" (default).
        """
        return await self._get_policies("nat", device_group, position)

    def _parse_policy_entries(self, raw: Any) -> list[dict]:
        """Extract policy entries from PanDirect response."""
        try:
            if isinstance(raw, dict):
                # Navigate to the entries
                entries = raw
                for key in ["result", "rules", "entry"]:
                    if isinstance(entries, dict) and key in entries:
                        entries = entries[key]
                if isinstance(entries, dict):
                    entries = [entries]
                if isinstance(entries, list):
                    return entries
            return [{"raw": str(raw)[:500]}]
        except Exception:
            return [{"raw": str(raw)[:500]}]

    # ------------------------------------------------------------------
    # Logs
    # ------------------------------------------------------------------
    async def _get_logs(self, log_type: str, query: str = "", limit: int = 100) -> list[dict]:
        """Query logs via PanDirect async enqueue/poll/retrieve pattern."""
        try:
            # Step 1: Enqueue the log request — returns a job ID
            enqueue_result = await self._run_direct(
                "MonitorDirect.enqueueLogRequest",
                [{"logType": log_type, "query": query, "nlogs": limit, "dir": "backward"}],
                timeout=30000,
            )
            # Extract job ID from response
            job_id = None
            if isinstance(enqueue_result, dict):
                job_id = (
                    enqueue_result.get("result", {}).get("job")
                    or enqueue_result.get("job")
                    or enqueue_result.get("result")
                )
            if job_id is None:
                return [{"error": f"Failed to enqueue log request: {str(enqueue_result)[:300]}"}]

            # Step 2: Poll until the log job is ready (max ~30 seconds)
            for _ in range(15):
                await asyncio.sleep(2)
                poll_result = await self._run_direct(
                    "MonitorDirect.pollLogRequest",
                    [{"jobId": job_id}],
                    timeout=15000,
                )
                if isinstance(poll_result, dict):
                    status = (
                        poll_result.get("result", {}).get("status")
                        or poll_result.get("status")
                    )
                    if status in ("completed", "FIN"):
                        break
            else:
                return [{"error": f"Log query timed out for job {job_id}"}]

            # Step 3: Retrieve the actual log entries
            raw = await self._run_direct(
                "MonitorDirect.retrieveJSONLog",
                [{"jobId": job_id}],
                timeout=30000,
            )
            try:
                entries = raw["result"]["log"]["logs"]["entry"]
                if isinstance(entries, dict):
                    entries = [entries]
                return entries
            except (KeyError, TypeError):
                # Try alternate response shapes
                if isinstance(raw, dict) and "result" in raw:
                    result = raw["result"]
                    if isinstance(result, list):
                        return result
                    if isinstance(result, dict):
                        for key in ["logs", "entries", "entry"]:
                            if key in result:
                                val = result[key]
                                if isinstance(val, dict):
                                    val = [val]
                                if isinstance(val, list):
                                    return val
                return [{"raw": str(raw)[:500]}]
        except Exception as e:
            return [{"error": str(e)}]

    async def get_traffic_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get traffic logs with optional filter."""
        return await self._get_logs("traffic", query, limit)

    async def get_threat_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get threat logs with optional filter."""
        return await self._get_logs("threat", query, limit)

    async def get_system_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get system logs with optional filter."""
        return await self._get_logs("system", query, limit)

    # ------------------------------------------------------------------
    # Operations
    # ------------------------------------------------------------------
    async def commit_changes(self, device_group: Optional[str] = None) -> dict:
        """Commit pending changes (validate first, then commit)."""
        try:
            # Validate first
            validate_params: dict[str, Any] = {}
            if device_group:
                validate_params["dg"] = device_group
            try:
                await self._run_direct("CommitDirect.validate", [validate_params])
            except Exception as ve:
                logger.debug("CommitDirect.validate failed (may be optional): %s", ve)

            # Run the actual commit
            commit_params: dict[str, Any] = {}
            if device_group:
                commit_params["dg"] = device_group
            raw = await self._run_direct("DeviceDirect.runCommitAll", [commit_params])
            return {"success": True, "result": raw}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def push_to_devices(self, device_group: str) -> dict:
        """Push configuration to devices in a device group."""
        try:
            raw = await self._run_direct(
                "DeviceDirect.runCommitAll",
                [{"dg": device_group}],
            )
            # Poll the job if we get a job ID back
            job_id = None
            if isinstance(raw, dict):
                job_id = (
                    raw.get("result", {}).get("job")
                    or raw.get("job")
                )
            if job_id:
                # Poll for completion (best-effort, don't fail if polling fails)
                try:
                    for _ in range(30):
                        await asyncio.sleep(2)
                        poll = await self._run_direct("PanDirect.pollJob", [{"jobId": job_id}])
                        if isinstance(poll, dict):
                            status = poll.get("result", {}).get("status") or poll.get("status")
                            if status in ("FIN", "completed"):
                                return {"success": True, "result": poll, "job_id": job_id}
                except Exception as pe:
                    logger.debug("Job polling failed: %s", pe)
            return {"success": True, "result": raw, "job_id": job_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================================================================
    # Tier 1 — confirmed PanDirect APIs
    # ==================================================================

    async def get_system_resources(self) -> dict:
        """Get Panorama system resource utilization (CPU, memory, disk)."""
        raw = await self._run_direct(
            "DashboardDirect.getSystemResources",
            [{"isCmsSelected": True, "isMultiVsys": False, "getTestXML": False, "vsysName": ""}],
        )
        try:
            return raw["result"]["data"]
        except (KeyError, TypeError):
            return raw if raw else {}

    async def get_templates(self) -> dict:
        """Get templates, template stacks, and device-group/template associations."""
        raw, method = await self._try_methods([
            ("PanoramaScalability.getDeviceGroupAndTemplateStatusMap", [{}]),
            ("DeviceDirect.getTemplateInfo", [{}]),
            ("DeviceDirect.getTemplateStackInfo", [{}]),
        ])
        if raw is None:
            return {"error": "No working method found for templates. Use panorama_discover_methods to find the correct API."}
        try:
            return raw["result"] if isinstance(raw, dict) and "result" in raw else raw
        except (KeyError, TypeError):
            return raw if raw else {}

    async def get_commit_history(self, limit: int = 50) -> list[dict]:
        """Get configuration commit audit trail."""
        raw = await self._run_direct(
            "ConfigAudit.getAllCommitVersionList",
            [{"nlogs": limit}],
        )
        try:
            entries = raw["result"]["entry"]
            if isinstance(entries, dict):
                entries = [entries]
            return entries
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}] if raw else []

    async def run_direct(self, method: str, params: list | None = None, timeout: int = 30000) -> Any:
        """
        Generic PanDirect RPC escape hatch.

        Call any Panos.direct.run() method directly.  Useful for exploring
        the API or calling methods not yet wrapped by dedicated tools.
        """
        return await self._run_direct(method, params, timeout)

    async def discover_methods(self, namespace: str = "") -> dict:
        """
        Discover available PanDirect RPC method names.

        Panos.direct.run() is a pure RPC dispatcher — method names are
        server-side strings, not JS objects.  Discovery works by scanning
        the loaded Panorama JS source files for direct.run() call patterns.

        If namespace is empty, lists all discoverable namespaces and methods.
        If a namespace is given (e.g. "DashboardDirect"), filters to that prefix.
        """
        if not self.session.page:
            raise RuntimeError("Browser not initialized")

        result = await self.session.page.evaluate(
            """(ns) => {
                const results = { methods: [], source: 'js_source_scan' };
                try {
                    // Collect all script sources loaded in the page
                    const scripts = document.querySelectorAll('script[src]');
                    const methodSet = new Set();

                    // Match: .run("Namespace.method" or .run('Namespace.method'
                    // Build regex via concatenation to avoid Python/JS quote conflicts
                    const q = '[' + String.fromCharCode(34, 39) + ']';
                    const patterns = [
                        new RegExp('[.]run[(]\\\\s*' + q + '([A-Z][A-Za-z]+[.][a-zA-Z]+)' + q, 'g'),
                    ];

                    // Scan inline scripts
                    const inlineScripts = document.querySelectorAll('script:not([src])');
                    for (const s of inlineScripts) {
                        const src = s.textContent || '';
                        for (const pat of patterns) {
                            pat.lastIndex = 0;
                            let m;
                            while ((m = pat.exec(src)) !== null) {
                                methodSet.add(m[1]);
                            }
                        }
                    }

                    // For external scripts, try fetching via XHR (same-origin)
                    const fetchPromises = [];
                    for (const s of scripts) {
                        const url = s.src;
                        if (!url) continue;
                        try {
                            const xhr = new XMLHttpRequest();
                            xhr.open('GET', url, false);  // synchronous
                            xhr.send();
                            if (xhr.status === 200) {
                                const src = xhr.responseText;
                                for (const pat of patterns) {
                                    pat.lastIndex = 0;
                                    let m;
                                    while ((m = pat.exec(src)) !== null) {
                                        methodSet.add(m[1]);
                                    }
                                }
                            }
                        } catch(e) {
                            // Skip CORS-blocked scripts
                        }
                    }

                    let methods = [...methodSet].sort();

                    // Filter by namespace if provided
                    if (ns) {
                        const nsLower = ns.toLowerCase();
                        methods = methods.filter(m => m.toLowerCase().startsWith(nsLower + '.'));
                        results.namespace = ns;
                    }

                    results.methods = methods;
                    results.total = methods.length;

                    // Extract namespaces
                    const namespaces = [...new Set(methods.map(m => m.split('.')[0]))].sort();
                    results.namespaces = namespaces;

                    return results;
                } catch(e) {
                    results.error = e.message;
                    return results;
                }
            }""",
            namespace,
        )
        return result

    # ==================================================================
    # Tier 2 — objects + network (method names use _try_methods fallback)
    # ==================================================================

    async def get_address_objects(self, device_group: str = "shared", search: str = "") -> list[dict]:
        """Get address objects for a device group with optional search filter."""
        params_base: dict[str, Any] = {"dg": device_group}
        if search:
            params_base["filter"] = search

        raw, method = await self._try_methods([
            ("ObjectsDirect.getAddresses", [params_base]),
            ("ObjectsDirect.getAll", [{**params_base, "type": "address"}]),
        ])
        if raw is None:
            return [{"error": "No working method found for address objects. Use panorama_discover_methods to find the correct API."}]
        try:
            entries = raw["result"]["entry"] if isinstance(raw, dict) else raw
            if isinstance(entries, dict):
                entries = [entries]
            return entries if isinstance(entries, list) else [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_service_objects(self, device_group: str = "shared", search: str = "") -> list[dict]:
        """Get service objects for a device group with optional search filter."""
        params_base: dict[str, Any] = {"dg": device_group}
        if search:
            params_base["filter"] = search

        raw, method = await self._try_methods([
            ("ObjectsDirect.getServices", [params_base]),
            ("ObjectsDirect.getAll", [{**params_base, "type": "service"}]),
        ])
        if raw is None:
            return [{"error": "No working method found for service objects. Use panorama_discover_methods to find the correct API."}]
        try:
            entries = raw["result"]["entry"] if isinstance(raw, dict) else raw
            if isinstance(entries, dict):
                entries = [entries]
            return entries if isinstance(entries, list) else [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_address_groups(self, device_group: str = "shared", search: str = "") -> list[dict]:
        """Get address group objects for a device group with optional search filter."""
        params_base: dict[str, Any] = {"dg": device_group}
        if search:
            params_base["filter"] = search

        raw, method = await self._try_methods([
            ("ObjectsDirect.getAddressGroups", [params_base]),
            ("ObjectsDirect.getAll", [{**params_base, "type": "address-group"}]),
        ])
        if raw is None:
            return [{"error": "No working method found for address groups. Use panorama_discover_methods to find the correct API."}]
        try:
            entries = raw["result"]["entry"] if isinstance(raw, dict) else raw
            if isinstance(entries, dict):
                entries = [entries]
            return entries if isinstance(entries, list) else [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_service_groups(self, device_group: str = "shared", search: str = "") -> list[dict]:
        """Get service group objects for a device group with optional search filter."""
        params_base: dict[str, Any] = {"dg": device_group}
        if search:
            params_base["filter"] = search

        raw, method = await self._try_methods([
            ("ObjectsDirect.getServiceGroups", [params_base]),
            ("ObjectsDirect.getAll", [{**params_base, "type": "service-group"}]),
        ])
        if raw is None:
            return [{"error": "No working method found for service groups. Use panorama_discover_methods to find the correct API."}]
        try:
            entries = raw["result"]["entry"] if isinstance(raw, dict) else raw
            if isinstance(entries, dict):
                entries = [entries]
            return entries if isinstance(entries, list) else [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_security_zones(self, template: str = "") -> list[dict]:
        """Get security zones, optionally scoped to a template."""
        params: dict[str, Any] = {"type": "zone"}
        if template:
            params["template"] = template

        raw, method = await self._try_methods([
            ("ObjectsDirect.getAll", [params]),
            ("ObjectsDirect.getZones", [params]),
        ])
        if raw is None:
            # Fallback: config API xpath
            try:
                xpath = "/config/devices/entry/vsys/entry/zone"
                if template:
                    xpath = f"/config/devices/entry/template/entry[@name='{template}']/config/devices/entry/vsys/entry/zone"
                config_result = await self._get_config(xpath)
                return [{"raw_config": str(config_result.get("text", ""))[:1000]}]
            except Exception:
                pass
            return [{"error": "No working method found for security zones. Use panorama_discover_methods to find the correct API."}]
        try:
            entries = raw["result"]["entry"] if isinstance(raw, dict) else raw
            if isinstance(entries, dict):
                entries = [entries]
            return entries if isinstance(entries, list) else [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_interfaces(self, template: str = "") -> list[dict]:
        """Get network interfaces, optionally scoped to a template."""
        params = {"template": template} if template else {}

        raw, method = await self._try_methods([
            ("NetworkDirect.getLinkStateMap", [params]),
            ("NetworkDirect.showAll", [params]),
        ])
        if raw is None:
            return [{"error": "No working method found for interfaces. Use panorama_discover_methods to find the correct API."}]
        try:
            result = raw["result"] if isinstance(raw, dict) and "result" in raw else raw
            if isinstance(result, dict):
                # getLinkStateMap may return a map rather than entry list
                if "entry" in result:
                    entries = result["entry"]
                    if isinstance(entries, dict):
                        entries = [entries]
                    return entries
                # Return the map directly
                return [result]
            if isinstance(result, list):
                return result
            return [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_routing(self, template: str = "") -> list[dict]:
        """Get routing information, optionally scoped to a template."""
        params = {"template": template} if template else {}

        raw, method = await self._try_methods([
            ("NetworkDirect.getVirtualRouterRunTimeStats", [params]),
            ("NetworkDirect.showAll", [params]),
        ])
        if raw is None:
            return [{"error": "No working method found for routing. Use panorama_discover_methods to find the correct API."}]
        try:
            result = raw["result"] if isinstance(raw, dict) and "result" in raw else raw
            if isinstance(result, dict):
                if "entry" in result:
                    entries = result["entry"]
                    if isinstance(entries, dict):
                        entries = [entries]
                    return entries
                return [result]
            if isinstance(result, list):
                return result
            return [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    # ==================================================================
    # Tier 3 — additional logs + monitoring
    # ==================================================================

    async def get_url_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get URL filtering logs."""
        return await self._get_logs("url", query, limit)

    async def get_wildfire_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get WildFire submission logs."""
        return await self._get_logs("wildfire", query, limit)

    async def get_config_logs(self, query: str = "", limit: int = 100) -> list[dict]:
        """Get configuration change logs."""
        return await self._get_logs("config", query, limit)

    async def get_jobs(self, status: str = "", limit: int = 50) -> list[dict]:
        """Get async job status (commits, pushes, upgrades)."""
        params: dict[str, Any] = {}
        if status:
            params["status"] = status
        if limit:
            params["nlogs"] = limit

        raw, method = await self._try_methods([
            ("MonitorDirect.getTasks", [params]),
            ("PanDirect.pollJobs", [params]),
        ])
        if raw is None:
            return [{"error": "No working method found for jobs. Use panorama_discover_methods to find the correct API."}]
        try:
            result = raw["result"] if isinstance(raw, dict) and "result" in raw else raw
            if isinstance(result, dict):
                if "entry" in result:
                    entries = result["entry"]
                    if isinstance(entries, dict):
                        entries = [entries]
                    return entries
                return [result]
            if isinstance(result, list):
                return result
            return [{"raw": str(raw)[:500]}]
        except (KeyError, TypeError):
            return [{"raw": str(raw)[:500]}]

    async def get_ha_status(self) -> dict:
        """Get high availability pair status."""
        raw, method = await self._try_methods([
            ("DeviceDirect.getHAConfig", [{}]),
            ("DeviceDirect.getHAMode", [{}]),
            ("DeviceDirect.getLocalState", [{}]),
        ])
        if raw is None:
            return {"error": "No working method found for HA status. Use panorama_discover_methods to find the correct API."}
        try:
            return raw["result"] if isinstance(raw, dict) and "result" in raw else raw
        except (KeyError, TypeError):
            return raw if raw else {}

    async def get_software_info(self) -> dict:
        """Get installed PAN-OS and content versions."""
        raw, method = await self._try_methods([
            ("Software.getUpgradeHistory", [{}]),
            ("DynamicUpdates.getDownloadedContent", [{}]),
            ("DeviceDirect.getLicensesList", [{}]),
        ])
        if raw is None:
            return {"error": "No working method found for software info. Use panorama_discover_methods to find the correct API."}
        try:
            return raw["result"] if isinstance(raw, dict) and "result" in raw else raw
        except (KeyError, TypeError):
            return raw if raw else {}
