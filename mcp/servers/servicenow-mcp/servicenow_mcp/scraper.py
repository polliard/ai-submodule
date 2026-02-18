"""
ServiceNow web scraper using Playwright.

Handles SSO authentication, navigation, and data extraction from ServiceNow UI.
Uses browser-based SSO - no username/password required.
"""

import os
import re
import stat
import time
from typing import Any, Dict, List, Optional
from contextlib import contextmanager

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class ServiceNowScraperError(Exception):
    """Base exception for scraper errors."""
    pass


class AuthenticationError(ServiceNowScraperError):
    """Authentication failed."""
    pass


class NavigationError(ServiceNowScraperError):
    """Failed to navigate to page."""
    pass


class ServiceNowScraper:
    """
    ServiceNow web scraper with SSO authentication.

    Automates browser to extract data from ServiceNow when API access
    is not available. Uses browser-based SSO authentication.
    """

    # Session storage location
    SESSION_DIR = os.path.expanduser("~/.config/servicenow-mcp")

    # Session expiry (8 hours - typical SSO session length)
    SESSION_MAX_AGE_SECONDS = 8 * 60 * 60

    # Common ServiceNow tables and their list URLs
    TABLES = {
        "incident": "incident_list.do",
        "change_request": "change_request_list.do",
        "problem": "problem_list.do",
        "cmdb_ci": "cmdb_ci_list.do",
        "cmdb_ci_server": "cmdb_ci_server_list.do",
        "cmdb_ci_app_server": "cmdb_ci_app_server_list.do",
        "cmdb_ci_database": "cmdb_ci_database_list.do",
        "sys_user": "sys_user_list.do",
        "sys_user_group": "sys_user_group_list.do",
        "kb_knowledge": "kb_knowledge_list.do",
        "task": "task_list.do",
        "sc_request": "sc_request_list.do",
        "sc_req_item": "sc_req_item_list.do",
    }

    def __init__(
        self,
        instance: Optional[str] = None,
        headless: bool = False,  # Default to visible for SSO
    ):
        """
        Initialize scraper with SSO authentication.

        Args:
            instance: ServiceNow instance (e.g., mycompany.service-now.com)
            headless: Run browser in headless mode (default False for SSO)
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ServiceNowScraperError(
                "Playwright not installed. Run: pip install playwright && playwright install chromium"
            )

        self.instance = instance or os.environ.get("SERVICENOW_INSTANCE", "")
        self.headless = headless

        if not self.instance:
            raise ServiceNowScraperError("SERVICENOW_INSTANCE not set")

        # Clean instance URL
        self.instance = self.instance.replace("https://", "").replace("http://", "").rstrip("/")
        self.base_url = f"https://{self.instance}"

        # Session file for this instance
        os.makedirs(self.SESSION_DIR, mode=0o700, exist_ok=True)
        self._session_file = os.path.join(
            self.SESSION_DIR,
            f"{self.instance.replace('.', '_')}_session.json"
        )

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._logged_in = False

    def _is_session_valid(self) -> bool:
        """Check if session file exists and is not expired."""
        if not os.path.exists(self._session_file):
            return False

        try:
            # Check session age
            file_age = time.time() - os.path.getmtime(self._session_file)
            if file_age > self.SESSION_MAX_AGE_SECONDS:
                # Session expired - remove it
                os.remove(self._session_file)
                return False
            return True
        except:
            return False

    def _save_session(self):
        """Save browser session for reuse with secure permissions."""
        if self._context:
            try:
                self._context.storage_state(path=self._session_file)
                # Set restrictive permissions (owner read/write only)
                os.chmod(self._session_file, stat.S_IRUSR | stat.S_IWUSR)  # 0600
            except:
                pass  # Best effort

    def _ensure_browser(self):
        """Ensure browser is started, reusing session if available."""
        if self._browser is None:
            self._playwright = sync_playwright().start()

            # Use headless mode if we have a valid session (no login needed)
            # or if explicitly requested
            use_headless = self.headless or self._is_session_valid()
            self._browser = self._playwright.chromium.launch(headless=use_headless)
            # Update headless flag to reflect actual state
            self.headless = use_headless

            context_options = {
                "viewport": {"width": 1920, "height": 1080},
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }

            # Try to reuse existing session
            if self._is_session_valid():
                try:
                    context_options["storage_state"] = self._session_file
                except:
                    pass  # Session file may be invalid

            self._context = self._browser.new_context(**context_options)
            self._page = self._context.new_page()

    def switch_to_headless(self):
        """
        Switch browser to headless mode after login.

        Closes the visible browser and relaunches in headless mode,
        reusing the saved session. This is useful after interactive
        login to avoid showing the browser during queries.
        """
        if not self._logged_in:
            return  # Only switch after successful login

        if self.headless:
            return  # Already headless, nothing to do

        # Save session before switching
        self._save_session()

        # Close visible browser
        if self._page:
            try:
                self._page.close()
            except:
                pass
            self._page = None

        if self._context:
            try:
                self._context.close()
            except:
                pass
            self._context = None

        if self._browser:
            try:
                self._browser.close()
            except:
                pass
            self._browser = None

        if self._playwright:
            try:
                self._playwright.stop()
            except:
                pass
            self._playwright = None

        # Relaunch in headless mode
        self.headless = True
        self._ensure_browser()

    def _is_logged_in(self) -> bool:
        """Check if currently logged in to ServiceNow by navigating to test page."""
        try:
            # Navigate to a simple page and check if redirected to login
            self._page.goto(f"{self.base_url}/nav_to.do", wait_until="networkidle", timeout=15000)
            return self._check_logged_in_on_current_page()
        except:
            return False

    def _check_logged_in_on_current_page(self) -> bool:
        """Check if current page indicates logged in state (doesn't navigate)."""
        try:
            current_url = self._page.url.lower()

            # If we're on login page or SSO page, not logged in
            if "login" in current_url or "saml" in current_url or "sso" in current_url:
                return False

            # Check if we're on the ServiceNow instance (not IDP)
            if self.instance.lower() not in current_url:
                return False

            # Check for ServiceNow navigation elements
            nav_element = self._page.query_selector(
                "iframe#gsft_main, .navpage-header, .sn-polaris-header, #nav_west_center, "
                ".sn-polaris-nav, #gsft_nav, .nav-body"
            )
            return nav_element is not None
        except:
            return False

    def _is_on_idp_page(self) -> bool:
        """Check if currently on an IDP/SSO page (not ServiceNow)."""
        try:
            current_url = self._page.url.lower()
            # Common IDP domains - expanded list
            idp_indicators = [
                "okta", "microsoftonline", "login.microsoft", "adfs", "ping",
                "auth0", "onelogin", "duo", "azure", "google.com/accounts",
                "sso.", "idp.", "identity.", "federation", "saml", "sts.",
                "login.windows.net", "accounts.google", "myworkdayjobs"
            ]
            # Also check if NOT on our ServiceNow instance
            if self.instance.lower() in current_url:
                return False
            return any(idp in current_url for idp in idp_indicators)
        except:
            return False

    def _is_on_servicenow_login(self) -> bool:
        """Check if on ServiceNow's login page (not IDP)."""
        try:
            current_url = self._page.url.lower()
            return self.instance.lower() in current_url and "login" in current_url
        except:
            return False

    def _click_sso_button(self) -> bool:
        """Try to find and click an SSO login button. Returns True if clicked."""
        try:
            # Common SSO button selectors
            sso_selectors = [
                "a[href*='sso']", "a[href*='saml']", "button:has-text('SSO')",
                "a:has-text('SSO')", "a:has-text('Single Sign')",
                "button:has-text('Single Sign')", "a:has-text('Use external')",
                "a:has-text('Company Login')", "a:has-text('Corporate')",
                "#sso_login", ".sso-login", "[data-sso]",
                "a:has-text('Log in with')", "button:has-text('Log in with')"
            ]
            for selector in sso_selectors:
                try:
                    btn = self._page.query_selector(selector)
                    if btn and btn.is_visible():
                        btn.click()
                        time.sleep(2)  # Wait for redirect
                        return True
                except:
                    continue
            return False
        except:
            return False

    def login_interactive(self, switch_headless: bool = True):
        """
        Interactive login - opens browser and waits for user to complete SSO.

        This is a standalone method for the 'login' CLI command.
        Doesn't interfere with the login process at all - just waits.

        Args:
            switch_headless: If True, switch to headless mode after login (default True)
        """
        self._ensure_browser()

        # Check if already logged in from saved session
        if self._is_logged_in():
            print("Already logged in from saved session!")
            self._logged_in = True
            if switch_headless:
                self.switch_to_headless()
            return

        # Navigate to ServiceNow - let it redirect to SSO naturally
        print(f"Opening {self.base_url}...")
        self._page.goto(self.base_url, wait_until="domcontentloaded", timeout=30000)

        print(f"\n{'='*60}")
        print("Complete SSO login in the browser window.")
        print("Press ENTER here when done (or Ctrl+C to cancel).")
        print(f"{'='*60}\n")

        # Wait for user to press Enter
        try:
            input("Press ENTER when login is complete...")
        except KeyboardInterrupt:
            raise AuthenticationError("Login cancelled by user")

        # Now check if they're actually logged in
        time.sleep(1)

        # Navigate to a ServiceNow page to verify
        try:
            self._page.goto(f"{self.base_url}/nav_to.do", wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
        except:
            pass

        if self._check_logged_in_on_current_page():
            self._logged_in = True
            self._save_session()
            print("Login verified and session saved!")
            # Switch to headless mode for subsequent queries
            if switch_headless:
                self.switch_to_headless()
        else:
            raise AuthenticationError("Login verification failed - please try again")

    def _login(self):
        """Log into ServiceNow via SSO."""
        if self._logged_in:
            return

        self._ensure_browser()

        # Check if already logged in from saved session
        if self._is_logged_in():
            self._logged_in = True
            return

        # No saved session - need interactive login
        # Navigate to ServiceNow - let it redirect naturally
        self._page.goto(self.base_url, wait_until="domcontentloaded", timeout=30000)

        print(f"\n{'='*60}")
        print("SSO Authentication Required")
        print(f"{'='*60}")
        print(f"A browser window has opened for: {self.base_url}")
        print("")
        print("Complete SSO login in the browser.")
        print("The script will wait until you're logged in.")
        print("")
        print("TIP: Run 'servicenow-mcp login' first to authenticate")
        print("     and save your session for later use.")
        print(f"{'='*60}\n")

        # Wait for successful login (up to 10 minutes for SSO)
        # IMPORTANT: Don't navigate or click anything - just watch the URL
        try:
            for i in range(600):  # 10 minutes with 1-second intervals
                time.sleep(1)

                try:
                    current_url = self._page.url
                except:
                    raise AuthenticationError("Browser was closed before login completed")

                # Progress update every minute
                if i > 0 and i % 60 == 0:
                    remaining = (600 - i) // 60
                    print(f"Waiting... {remaining} min remaining")

                # Check if on ServiceNow (not login page) and has nav elements
                if self.instance.lower() in current_url.lower():
                    if "login" not in current_url.lower() and "saml" not in current_url.lower():
                        # Might be logged in - verify with a quick check
                        if self._check_logged_in_on_current_page():
                            self._logged_in = True
                            self._save_session()
                            print("\nSSO authentication successful! Session saved.")
                            # Switch to headless mode for subsequent queries
                            self.switch_to_headless()
                            return

            raise AuthenticationError("SSO authentication timed out after 10 minutes")

        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            raise AuthenticationError(f"SSO login failed: {e}")

    def _navigate_to_list(
        self, table: str, query: Optional[str] = None, offset: int = 0
    ) -> Page:
        """
        Navigate to a table list view.

        Args:
            table: Table name (e.g., 'incident', 'cmdb_ci_server')
            query: Optional encoded query string
            offset: Starting row for pagination (0-indexed)

        Returns:
            Page object positioned at the list
        """
        self._login()

        # Build URL with pagination support
        list_url = self.TABLES.get(table, f"{table}_list.do")
        url = f"{self.base_url}/{list_url}"

        params = []
        if query:
            params.append(f"sysparm_query={query}")
        if offset > 0:
            params.append(f"sysparm_first_row={offset}")

        if params:
            url += "?" + "&".join(params)

        self._page.goto(url, wait_until="networkidle")

        # ServiceNow often uses iframes - check if we need to switch
        main_frame = self._page

        # Look for gsft_main iframe (common in ServiceNow)
        iframe = self._page.query_selector("iframe#gsft_main, iframe[name='gsft_main']")
        if iframe:
            main_frame = iframe.content_frame()

        # Wait for list to load
        try:
            main_frame.wait_for_selector(
                ".list2_body, .list_table, table.list_table, .data_list_table",
                timeout=15000
            )
        except:
            # May be workspace UI
            main_frame.wait_for_selector(
                "[data-testid='list-layout'], .list-component, .sn-list",
                timeout=10000
            )

        return main_frame

    def _parse_list_table(self, frame: Page, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Parse a ServiceNow list table.

        Handles the info column (?) at the start of each row.

        Args:
            frame: Page/frame containing the list
            limit: Maximum rows to return

        Returns:
            List of row dictionaries
        """
        rows = []

        # Try different table selectors (classic vs workspace UI)
        table = frame.query_selector(
            ".list2_body table, table.list_table, .data_list_table table, "
            "[data-testid='list-layout'] table"
        )

        if not table:
            # Try workspace/next experience UI
            return self._parse_workspace_list(frame, limit)

        # Get headers
        headers = []
        header_row = table.query_selector("thead tr, tr.list_header, tr.header_row")
        if header_row:
            header_cells = header_row.query_selector_all("th, td")
            for i, cell in enumerate(header_cells):
                text = cell.inner_text().strip()
                # First column is often info/action icons - skip or mark it
                if i == 0 and (not text or text in ["", " ", "i", "?"]):
                    headers.append("_info_column")
                else:
                    headers.append(text or f"col_{i}")

        # Get data rows
        data_rows = table.query_selector_all("tbody tr, tr.list_row, tr.list_odd, tr.list_even")

        for row in data_rows[:limit]:
            cells = row.query_selector_all("td")
            row_data = {}

            for i, cell in enumerate(cells):
                if i >= len(headers):
                    break

                header = headers[i]

                # Skip info column but extract sys_id from link if present
                if header == "_info_column":
                    link = cell.query_selector("a")
                    if link:
                        href = link.get_attribute("href") or ""
                        sys_id_match = re.search(r'sys_id=([a-f0-9]{32})', href)
                        if sys_id_match:
                            row_data["sys_id"] = sys_id_match.group(1)
                    continue

                # Get cell value
                link = cell.query_selector("a")
                if link:
                    row_data[header] = link.inner_text().strip()
                    # Extract sys_id from link
                    href = link.get_attribute("href") or ""
                    sys_id_match = re.search(r'sys_id=([a-f0-9]{32})', href)
                    if sys_id_match and "sys_id" not in row_data:
                        row_data["sys_id"] = sys_id_match.group(1)
                else:
                    row_data[header] = cell.inner_text().strip()

            if row_data:
                rows.append(row_data)

        return rows

    def _parse_workspace_list(self, frame: Page, limit: int = 50) -> List[Dict[str, Any]]:
        """Parse workspace/next experience UI list."""
        rows = []

        # Workspace UI uses different structure
        list_items = frame.query_selector_all(
            "[data-testid='list-row'], .list-row, .sn-list-row"
        )

        for item in list_items[:limit]:
            row_data = {}

            # Extract fields from list item
            fields = item.query_selector_all("[data-testid='cell'], .list-cell, .field-value")
            for field in fields:
                label = field.get_attribute("data-label") or field.get_attribute("aria-label") or ""
                value = field.inner_text().strip()
                if label and value:
                    row_data[label] = value

            # Try to get sys_id from row
            sys_id = item.get_attribute("data-sys-id") or item.get_attribute("data-record-id")
            if sys_id:
                row_data["sys_id"] = sys_id

            if row_data:
                rows.append(row_data)

        return rows

    def _navigate_to_record(self, table: str, identifier: str) -> Page:
        """
        Navigate to a specific record.

        Args:
            table: Table name
            identifier: sys_id or record number (e.g., INC0012345)

        Returns:
            Page/frame positioned at the record
        """
        self._login()

        # Determine if identifier is sys_id or number
        if re.match(r'^[a-f0-9]{32}$', identifier):
            url = f"{self.base_url}/{table}.do?sys_id={identifier}"
        else:
            # Search by number field
            url = f"{self.base_url}/{table}.do?sysparm_query=number={identifier}"

        self._page.goto(url, wait_until="networkidle")

        # Handle iframe
        main_frame = self._page
        iframe = self._page.query_selector("iframe#gsft_main, iframe[name='gsft_main']")
        if iframe:
            main_frame = iframe.content_frame()

        # Wait for form to load
        main_frame.wait_for_selector(
            "form[name='form'], .form-group, [data-testid='record-form']",
            timeout=15000
        )

        return main_frame

    def _parse_record_form(self, frame: Page) -> Dict[str, Any]:
        """
        Parse a ServiceNow record form.

        Args:
            frame: Page/frame containing the form

        Returns:
            Dictionary of field name -> value
        """
        record = {}

        # Classic UI form fields
        form = frame.query_selector("form[name='form'], form.form-horizontal")
        if form:
            # Get all form groups/fields
            groups = form.query_selector_all(
                ".form-group, .form_field, tr[id^='element.'], "
                ".section_header_content_no_scroll tr"
            )

            for group in groups:
                # Get label
                label_el = group.query_selector(
                    "label, .label, .control-label, span.label_text"
                )
                if not label_el:
                    continue

                label = label_el.inner_text().strip().rstrip(":")
                if not label:
                    continue

                # Get value - try different selectors
                value = ""

                # Input field
                input_el = group.query_selector(
                    "input:not([type='hidden']), select, textarea"
                )
                if input_el:
                    value = input_el.input_value() or input_el.get_attribute("value") or ""

                # Display value (read-only)
                if not value:
                    display_el = group.query_selector(
                        ".form-control-static, .display_value, "
                        "span.readonly, a.linked"
                    )
                    if display_el:
                        value = display_el.inner_text().strip()

                # Reference field display
                if not value:
                    ref_el = group.query_selector(".ref_readonly, .reference")
                    if ref_el:
                        value = ref_el.inner_text().strip()

                if label and value:
                    record[label] = value

        # Also try workspace/next experience UI
        if not record:
            field_groups = frame.query_selector_all(
                "[data-testid='form-field'], .form-field, .sn-form-field"
            )
            for group in field_groups:
                label_el = group.query_selector("[data-testid='label'], .field-label")
                value_el = group.query_selector("[data-testid='value'], .field-value")

                if label_el and value_el:
                    label = label_el.inner_text().strip()
                    value = value_el.inner_text().strip()
                    if label and value:
                        record[label] = value

        return record

    def query_table(
        self,
        table: str,
        query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        fetch_all: bool = False,
        page_size: int = 200,
        max_records: int = 10000,
    ) -> Dict[str, Any]:
        """
        Query a ServiceNow table with pagination support.

        Args:
            table: Table name
            query: Encoded query string (e.g., "priority=1^state!=7")
            limit: Maximum records to return (ignored if fetch_all=True)
            offset: Starting row for pagination (0-indexed)
            fetch_all: If True, automatically paginate to fetch all records
            page_size: Records per page when fetch_all=True (default: 200)
            max_records: Safety limit when fetch_all=True (default: 10000)

        Returns:
            Dictionary with records and metadata:
            {
                "records": [...],
                "total_fetched": int,
                "offset": int,
                "truncated": bool,  # True if max_records limit hit
                "page_count": int   # Number of pages fetched (1 if not fetch_all)
            }
        """
        if fetch_all:
            # Auto-paginate to fetch all records
            all_records = []
            current_offset = offset
            page_count = 0

            while len(all_records) < max_records:
                frame = self._navigate_to_list(table, query, current_offset)
                page_records = self._parse_list_table(frame, page_size)
                page_count += 1

                if not page_records:
                    # No more records
                    break

                all_records.extend(page_records)

                if len(page_records) < page_size:
                    # Last page - fewer records than page_size
                    break

                current_offset += len(page_records)

            # Truncate to max_records if exceeded
            truncated = len(all_records) > max_records
            if truncated:
                all_records = all_records[:max_records]

            return {
                "records": all_records,
                "total_fetched": len(all_records),
                "offset": offset,
                "truncated": truncated,
                "page_count": page_count,
            }
        else:
            # Single page query
            frame = self._navigate_to_list(table, query, offset)
            records = self._parse_list_table(frame, limit)
            return {
                "records": records,
                "total_fetched": len(records),
                "offset": offset,
                "truncated": False,
                "page_count": 1,
            }

    def describe_table(self, table: str) -> Dict[str, Any]:
        """
        Get field information for a ServiceNow table.

        Queries sys_dictionary to get field names, types, and descriptions.

        Args:
            table: Table name (e.g., 'incident', 'cmdb_ci_business_app')

        Returns:
            Dictionary with table metadata and fields:
            {
                "table": str,
                "fields": [
                    {"name": str, "label": str, "type": str, "mandatory": bool}
                ]
            }
        """
        # Query sys_dictionary for this table's fields
        dict_query = f"name={table}^elementISNOTEMPTY"
        frame = self._navigate_to_list("sys_dictionary", dict_query)
        raw_fields = self._parse_list_table(frame, 500)

        # Also get inherited fields from parent tables
        # by checking for fields where name starts with table base class

        fields = []
        seen = set()

        for row in raw_fields:
            # Map common column names from sys_dictionary
            field_name = row.get("Column name", row.get("Element", ""))
            field_label = row.get("Column label", row.get("Label", field_name))
            field_type = row.get("Type", "")
            mandatory = row.get("Mandatory", "").lower() == "true"

            if field_name and field_name not in seen:
                seen.add(field_name)
                fields.append({
                    "name": field_name,
                    "label": field_label,
                    "type": field_type,
                    "mandatory": mandatory,
                })

        # Sort by name for easier reading
        fields.sort(key=lambda f: f["name"])

        return {
            "table": table,
            "field_count": len(fields),
            "fields": fields,
        }

    @staticmethod
    def build_query(filters: List[Dict[str, Any]], operator: str = "AND") -> str:
        """
        Build an encoded query string from structured filters.

        Converts a list of filter conditions to ServiceNow's encoded query syntax.

        Args:
            filters: List of filter dictionaries, each with:
                - field: Field name (e.g., "operational_status", "u_lob")
                - operator: Comparison operator
                    - "=", "!=", ">", ">=", "<", "<="
                    - "LIKE", "STARTSWITH", "ENDSWITH"
                    - "IN", "NOT IN" (value should be comma-separated)
                    - "ISEMPTY", "ISNOTEMPTY"
                - value: Value to compare (not needed for ISEMPTY/ISNOTEMPTY)
            operator: Logical operator between conditions ("AND" or "OR")

        Returns:
            Encoded query string (e.g., "u_lob=SET^operational_status!=retired")

        Example:
            filters = [
                {"field": "u_lob", "operator": "=", "value": "SET"},
                {"field": "operational_status", "operator": "!=", "value": "retired"},
                {"field": "name", "operator": "LIKE", "value": "prod"},
            ]
            query = ServiceNowScraper.build_query(filters)
            # Returns: "u_lob=SET^operational_status!=retired^nameLIKEprod"
        """
        join_char = "^" if operator.upper() == "AND" else "^OR"
        parts = []

        for f in filters:
            field = f.get("field", "")
            op = f.get("operator", "=")
            value = f.get("value", "")

            if not field:
                continue

            # Handle different operators
            op_upper = op.upper()

            if op_upper in ("ISEMPTY", "ISNOTEMPTY"):
                parts.append(f"{field}{op_upper}")
            elif op_upper == "IN":
                parts.append(f"{field}IN{value}")
            elif op_upper == "NOT IN":
                parts.append(f"{field}NOTIN{value}")
            elif op_upper in ("LIKE", "STARTSWITH", "ENDSWITH"):
                parts.append(f"{field}{op_upper}{value}")
            elif op_upper in ("=", "!=", ">", ">=", "<", "<="):
                parts.append(f"{field}{op}{value}")
            else:
                # Default to equals
                parts.append(f"{field}={value}")

        return join_char.join(parts)

    def get_record(self, table: str, identifier: str) -> Dict[str, Any]:
        """
        Get a specific record.

        Args:
            table: Table name
            identifier: sys_id or record number

        Returns:
            Record dictionary
        """
        frame = self._navigate_to_record(table, identifier)
        return self._parse_record_form(frame)

    def search_knowledge(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search the knowledge base.

        Args:
            query: Search text
            limit: Maximum results

        Returns:
            List of KB articles
        """
        self._login()

        # Navigate to KB search
        url = f"{self.base_url}/kb_find.do?sysparm_search={query}"
        self._page.goto(url, wait_until="networkidle")

        # Handle iframe
        main_frame = self._page
        iframe = self._page.query_selector("iframe#gsft_main")
        if iframe:
            main_frame = iframe.content_frame()

        # Wait for results
        time.sleep(2)  # KB search can be slow

        results = []

        # Parse search results
        articles = main_frame.query_selector_all(
            ".kb_article, .search_result, .kb-result, "
            "[data-testid='search-result']"
        )

        for article in articles[:limit]:
            result = {}

            # Title
            title_el = article.query_selector(
                ".kb_title, .result_title, h3, a.kb-article-link"
            )
            if title_el:
                result["title"] = title_el.inner_text().strip()
                link = title_el if title_el.tag_name == "a" else title_el.query_selector("a")
                if link:
                    href = link.get_attribute("href") or ""
                    sys_id_match = re.search(r'sys_id=([a-f0-9]{32})', href)
                    if sys_id_match:
                        result["sys_id"] = sys_id_match.group(1)

            # Snippet/description
            snippet_el = article.query_selector(
                ".kb_short_description, .result_snippet, .kb-snippet"
            )
            if snippet_el:
                result["short_description"] = snippet_el.inner_text().strip()

            # Category
            cat_el = article.query_selector(".kb_category, .category")
            if cat_el:
                result["category"] = cat_el.inner_text().strip()

            if result:
                results.append(result)

        return results

    def close(self):
        """Close browser and cleanup."""
        if self._page:
            self._page.close()
            self._page = None
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            self._playwright = None
        self._logged_in = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
