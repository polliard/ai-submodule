"""
ServiceNow web scraper using Playwright.

Handles authentication, navigation, and data extraction from ServiceNow UI.
"""

import os
import re
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
    is not available.
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

    def __init__(
        self,
        instance: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        headless: bool = True,
    ):
        """
        Initialize scraper.

        Args:
            instance: ServiceNow instance (e.g., mycompany.service-now.com)
            username: ServiceNow username
            password: ServiceNow password
            headless: Run browser in headless mode
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ServiceNowScraperError(
                "Playwright not installed. Run: pip install playwright && playwright install chromium"
            )

        self.instance = instance or os.environ.get("SERVICENOW_INSTANCE", "")
        self.username = username or os.environ.get("SERVICENOW_USERNAME", "")
        self.password = password or os.environ.get("SERVICENOW_PASSWORD", "")
        self.headless = headless

        if not self.instance:
            raise ServiceNowScraperError("SERVICENOW_INSTANCE not set")
        if not self.username:
            raise ServiceNowScraperError("SERVICENOW_USERNAME not set")
        if not self.password:
            raise ServiceNowScraperError("SERVICENOW_PASSWORD not set")

        # Clean instance URL
        self.instance = self.instance.replace("https://", "").replace("http://", "").rstrip("/")
        self.base_url = f"https://{self.instance}"

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._logged_in = False

    def _ensure_browser(self):
        """Ensure browser is started."""
        if self._browser is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=self.headless)
            self._context = self._browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            self._page = self._context.new_page()

    def _login(self):
        """Log into ServiceNow."""
        if self._logged_in:
            return

        self._ensure_browser()

        # Navigate to login page
        self._page.goto(f"{self.base_url}/login.do", wait_until="networkidle")

        # Wait for login form
        try:
            # Standard ServiceNow login
            self._page.wait_for_selector("#user_name, input[name='user_name']", timeout=10000)

            # Fill credentials
            self._page.fill("#user_name, input[name='user_name']", self.username)
            self._page.fill("#user_password, input[name='user_password']", self.password)

            # Submit
            self._page.click("#sysverb_login, button[type='submit'], input[type='submit']")

            # Wait for navigation to complete (should redirect to home/dashboard)
            self._page.wait_for_load_state("networkidle", timeout=30000)

            # Check if login succeeded (look for navigator or home frame)
            if "login" in self._page.url.lower() and "sso" not in self._page.url.lower():
                # Still on login page - check for error
                error = self._page.query_selector(".error, .alert-danger, #status")
                if error:
                    raise AuthenticationError(f"Login failed: {error.inner_text()}")
                raise AuthenticationError("Login failed: still on login page")

            self._logged_in = True

        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            raise AuthenticationError(f"Login failed: {e}")

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
