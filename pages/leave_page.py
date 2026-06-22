from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from utils.wait_helpers import wait_present, wait_visible, wait_url_contains
"""Page object for Leave list, filters, and assign leave actions."""


class LeavePage(BasePage):
    LOC_PAGE_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")

    LOC_LEAVE_TYPE = (By.XPATH, "//label[normalize-space()='Leave Type']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
    LOC_LEAVE_STATUS = (By.XPATH, "//label[normalize-space()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
    LOC_FROM_DATE = (By.XPATH, "//label[normalize-space()='From Date']/../following-sibling::div//input")
    LOC_TO_DATE = (By.XPATH, "//label[normalize-space()='To Date']/../following-sibling::div//input")
    LOC_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    LOC_NO_RECORDS = (By.XPATH, "//*[normalize-space()='No Records Found']")
    LOC_TABLE_ROWS = (By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[@role='row']")
    LOC_DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='listbox']//span[normalize-space()]")
    LOC_EMPLOYEE_NAME = (By.XPATH, "//label[normalize-space()='Employee Name']/../following-sibling::div//input")

    LOC_ASSIGN_BUTTON = (By.XPATH, "//button[normalize-space()='Assign Leave'] | //a[normalize-space()='Assign Leave']")
    LOC_ASSIGN_EMPLOYEE = (By.XPATH, "//label[normalize-space()='Employee Name']/../following-sibling::div//input")
    LOC_ASSIGN_LEAVE_TYPE = (By.XPATH, "//label[normalize-space()='Leave Type']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
    LOC_ASSIGN_FROM = (By.XPATH, "//label[normalize-space()='From Date']/../following-sibling::div//input")
    LOC_ASSIGN_TO = (By.XPATH, "//label[normalize-space()='To Date']/../following-sibling::div//input")
    LOC_ASSIGN_SUBMIT = (By.XPATH, "//button[normalize-space()='Assign'] | //button[normalize-space()='Submit']")
    LOC_ASSIGN_CONFIRM = (By.XPATH, "//div[contains(@class,'oxd-toast-container')]//p | //div[contains(normalize-space(),'Successfully')]")

    def get_header_text(self) -> str:
        return wait_visible(self.driver, *self.LOC_PAGE_HEADER, self.timeout).text.strip()

    def is_leave_list_loaded(self) -> bool:
        try:
            try:
                wait_url_contains(self.driver, "/leave/viewLeaveList", self.timeout)
            except Exception:
                wait_url_contains(self.driver, "/leave", self.timeout)

            try:
                wait_visible(self.driver, *self.LOC_TABLE_ROWS, self.timeout)
                return True
            except Exception:
                try:
                    return self.is_visible(*self.LOC_NO_RECORDS)
                except Exception:
                    try:
                        hdr = wait_visible(self.driver, *self.LOC_PAGE_HEADER, self.timeout)
                        return "leave" in hdr.text.strip().lower()
                    except Exception:
                        return False
        except Exception:
            return False

    def wait_for_search_results(self) -> None:
        # Wait until search results are ready: rows present, 'No Records', or visible errors
        def ready(d):
            rows = d.find_elements(*self.LOC_TABLE_ROWS)
            if any(r.is_displayed() and r.text.strip() for r in rows):
                return True

            try:
                nodes = d.find_elements(*self.LOC_NO_RECORDS)
                if any(n.is_displayed() for n in nodes):
                    return True
            except Exception:
                pass

            try:
                errors = d.find_elements(*self.LOC_REQUIRED_ERRORS)
                if any(e.is_displayed() and e.text.strip() for e in errors):
                    return True
            except Exception:
                pass

            return False

        WebDriverWait(self.driver, self.timeout).until(ready)



    def select_first_dropdown_option(self, dropdown_locator: tuple) -> str:
        # click dropdown
        try:
            self.action_click(*dropdown_locator)
        except Exception:
            try:
                self.action_js_click(*dropdown_locator)
            except Exception:
                # last resort: continue and try to detect visible listboxes
                pass

        # wait until a visible listbox appears and return its valid options
        def get_visible_options(driver):
            all_lists = driver.find_elements(By.XPATH, "//div[@role='listbox']")
            visible_lists = [l for l in all_lists if l.is_displayed()]

            if not visible_lists:
                return False

            # prefer the most recently visible list (some UIs render multiple)
            active = visible_lists[-1]
            options = active.find_elements(By.XPATH, ".//span[normalize-space()]")
            valid = [
                o for o in options
                if o.is_displayed() and o.text.strip() and o.text.strip().lower() not in ("-- select --", "select", "please select", "- select -")
            ]

            return valid if valid else False

        options = WebDriverWait(self.driver, self.timeout).until(get_visible_options)
        first = options[0]
        text = first.text.strip()
        try:
            first.click()
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", first)
            except Exception:
                pass

        return text

    def select_first_dropdown_option_and_search(self, dropdown_locator: tuple) -> str:
        text = self.select_first_dropdown_option(dropdown_locator)

        # wait overlay gone before clicking search
        try:
            self.action_dismiss_blocking_overlays()
        except Exception:
            pass

        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()
        return text

    def get_table_row_texts(self) -> list[str]:
        # Ensure search results have settled (rows present, 'No Records', or validation)
        try:
            self.wait_for_search_results()
        except Exception:
            # continue to attempt to read rows even if waiter timed out
            pass

        try:
            rows = self.driver.find_elements(*self.LOC_TABLE_ROWS)
        except Exception:
            return []

        return [r.text.strip() for r in rows if r.is_displayed() and r.text.strip()]

    def apply_date_filter(self, from_date: str, to_date: str) -> None:
        try:
            self.action_clear_and_type(*self.LOC_FROM_DATE, from_date)
        except Exception:
            el = self.driver.find_element(*self.LOC_FROM_DATE)
            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, from_date)

        try:
            self.action_clear_and_type(*self.LOC_TO_DATE, to_date)
        except Exception:
            el = self.driver.find_element(*self.LOC_TO_DATE)
            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, to_date)

        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def search_by_employee_name(self, name: str) -> None:
        if self.is_visible(*self.LOC_EMPLOYEE_NAME):
            self.action_clear_and_type(*self.LOC_EMPLOYEE_NAME, name)
            try:
                # attempt to blur/commit the typed name to trigger validation/autocomplete
                el = self.driver.find_element(*self.LOC_EMPLOYEE_NAME)
                el.send_keys(Keys.TAB)
            except Exception:
                pass
        else:
            el = self.driver.find_element(*self.LOC_EMPLOYEE_NAME)
            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, name)
        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def is_no_records_found_visible(self) -> bool:
        try:
            if self.is_visible(*self.LOC_NO_RECORDS):
                return True
        except Exception:
            pass

        try:
            rows = self.driver.find_elements(*self.LOC_TABLE_ROWS)
            visible_rows = [r for r in rows if r.is_displayed() and r.text.strip()]
            if not visible_rows:
                return True
        except Exception:
            pass

        return False


    def open_assign_leave(self) -> None:
        try:
            self.action_click(*self.LOC_ASSIGN_BUTTON)
        except Exception:
            pass

    def is_assign_form_loaded(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_ASSIGN_EMPLOYEE, self.timeout)
            wait_visible(self.driver, *self.LOC_ASSIGN_LEAVE_TYPE, self.timeout)
            wait_visible(self.driver, *self.LOC_ASSIGN_FROM, self.timeout)
            wait_visible(self.driver, *self.LOC_ASSIGN_TO, self.timeout)
            return True
        except Exception:
            return False

    def assign_leave(self, employee: str | None, leave_type: str | None, from_date: str, to_date: str) -> None:
        if employee:
            try:
                self.action_clear_and_type(*self.LOC_ASSIGN_EMPLOYEE, employee)
                try:
                    option = WebDriverWait(self.driver, self.timeout).until(
                        lambda d: next(
                            (
                                x
                                for x in d.find_elements(*self.LOC_DROPDOWN_OPTIONS)
                                if x.is_displayed() and x.text.strip() and x.text.strip().lower() not in ("-- select --", "select", "please select", "- select -")
                            ),
                            None,
                        )
                    )
                    if option:
                        try:
                            option.click()
                        except Exception:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
                                option,
                            )
                except Exception:
                    pass
            except Exception:
                el = self.driver.find_element(*self.LOC_ASSIGN_EMPLOYEE)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, employee)

        if leave_type:
            self.select_first_dropdown_option(self.LOC_ASSIGN_LEAVE_TYPE)

        try:
            self.action_clear_and_type(*self.LOC_ASSIGN_FROM, from_date)
            self.action_clear_and_type(*self.LOC_ASSIGN_TO, to_date)
        except Exception:
            try:
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", self.driver.find_element(*self.LOC_ASSIGN_FROM), from_date)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", self.driver.find_element(*self.LOC_ASSIGN_TO), to_date)
            except Exception:
                pass

        self.action_click(*self.LOC_ASSIGN_SUBMIT)
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: bool(d.find_elements(*self.LOC_ASSIGN_CONFIRM))
            )
        except Exception:
            pass


    def get_assign_confirmation_text(self) -> str:
        try:
            return wait_visible(self.driver, *self.LOC_ASSIGN_CONFIRM, self.timeout).text.strip()
        except Exception:
            return ""
