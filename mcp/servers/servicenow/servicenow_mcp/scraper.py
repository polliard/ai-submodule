"""
ServiceNow web scraper using Playwright.

Handles authentication, navigation, and data extraction from ServiceNow UI.
"""

import os
import re
import stat
import sys
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
    ServiceNow web scraper.

    Automates browser to extract data from ServiceNow when API access
    is not available. Uses SSO login - opens a visible browser for user
    to authenticate, then uses that session.
    """

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

    # Session storage location
    SESSION_DIR = os.path.expanduser("~/.config/servicenow-mcp")

    # Session expiry (8 hours - typical SSO session length)
    SESSION_MAX_AGE_SECONDS = 8 * 60 * 60

    def __init__(
        self,
        instance: Optional[str] = None,
    ):
        """
        Initialize scraper.

        Args:
            instance: ServiceNow instance (e.g., mycompany.service-now.com)
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ServiceNowScraperError(
                "Playwright not installed. Run: pip install playwright && playwright install chromium"
            )

        self.instance = instance or os.environ.get("SERVICENOW_INSTANCE", "")

        if not self.instance:
            raise ServiceNowScraperError("SERVICENOW_INSTANCE not set")

        # Clean instance URL
        self.instance = self.instance.replace("https://", "").replace("http://", "").rstrip("/")
        self.base_url = f"https://{self.instance}"

        # Session file for this instance
        os.makedirs(self.SESSION_DIR, exist_ok=True)
        self._session_file = os.path.join(self.SESSION_DIR, f"{self.instance.replace('.', '_')}_session.json")

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._logged_in = False

    def _ensure_browser(self, headless: bool = True):
        """Ensure browser is started."""
        if self._browser is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=headless)

            # Try to load existing session
            context_options = {
                "viewport": {"width": 1920, "height": 1080},
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }

            if self._is_session_valid():
                try:
                    context_options["storage_state"] = self._session_file
                except:
                    pass  # Session file may be invalid

            self._context = self._browser.new_context(**context_options)
            self._page = self._context.new_page()

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

    def _is_logged_in(self) -> bool:
        """Check if we're logged into ServiceNow."""
        try:
            # Navigate to a simple page to check auth status
            self._page.goto(f"{self.base_url}/navpage.do", wait_until="networkidle", timeout=10000)

            # If we get redirected to login/SSO, we're not logged in
            current_url = self._page.url.lower()
            if "login" in current_url or "sso" in current_url or "saml" in current_url or "oauth" in current_url:
                return False

            # Check for ServiceNow UI elements that indicate we're logged in
            logged_in_indicators = [
                "iframe#gsft_main",      # Classic UI
                ".sn-polaris-navigation", # Polaris UI
                ".navpage-header",        # Nav header
                "#nav_west_center",       # Navigator
            ]

            for selector in logged_in_indicators:
                if self._page.query_selector(selector):
                    return True

            return False
        except:
            return False

    def _login(self):
        """Log into ServiceNow via SSO."""
        if self._logged_in:
            return

        # First try with existing session (headless)
        self._ensure_browser(headless=True)

        if self._is_logged_in():
            self._logged_in = True
            return

        # Close headless browser and open visible one for SSO
        self.close()
        self._ensure_browser(headless=False)

        # Navigate to ServiceNow - will redirect to SSO
        self._page.goto(f"{self.base_url}/navpage.do", wait_until="networkidle")

        # Print message to stderr so user knows to login
        print(f"\n>>> Browser opened for SSO login to {self.instance}", file=sys.stderr)
        print(f">>> Please complete the login in the browser window...", file=sys.stderr)
        print(f">>> The browser will close automatically once logged in.\n", file=sys.stderr)

        # Wait for user to complete SSO login (up to 5 minutes)
        try:
            max_wait = 300  # 5 minutes
            start_time = time.time()

            while time.time() - start_time < max_wait:
                time.sleep(2)  # Check every 2 seconds

                current_url = self._page.url.lower()

                # Check if we're back on ServiceNow (not SSO/login)
                if self.instance.lower() in current_url:
                    if "login" not in current_url and "sso" not in current_url and "saml" not in current_url:
                        # Verify we're actually logged in
                        self._page.wait_for_load_state("networkidle", timeout=5000)

                        logged_in_indicators = [
                            "iframe#gsft_main",
                            ".sn-polaris-navigation",
                            ".navpage-header",
                            "#nav_west_center",
                        ]

                        for selector in logged_in_indicators:
                            if self._page.query_selector(selector):
                                print(f">>> Login successful!", file=sys.stderr)
                                self._save_session()
                                self._logged_in = True

                                # Reopen in headless mode for actual work
                                self.close()
                                self._ensure_browser(headless=True)
                                return

            raise AuthenticationError("Login timeout - please try again")

        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            raise AuthenticationError(f"SSO login failed: {e}")

    def _navigate_to_list(self, table: str, query: Optional[str] = None) -> Page:
        """
        Navigate to a table list view.

        Args:
            table: Table name (e.g., 'incident', 'cmdb_ci_server')
            query: Optional encoded query string

        Returns:
            Page object positioned at the list
        """
        self._login()

        # Build URL
        list_url = self.TABLES.get(table, f"{table}_list.do")
        url = f"{self.base_url}/{list_url}"

        if query:
            url += f"?sysparm_query={query}"

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
    ) -> List[Dict[str, Any]]:
        """
        Query a ServiceNow table.

        Args:
            table: Table name
            query: Encoded query string (e.g., "priority=1^state!=7")
            limit: Maximum records to return

        Returns:
            List of records
        """
        frame = self._navigate_to_list(table, query)
        return self._parse_list_table(frame, limit)

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
