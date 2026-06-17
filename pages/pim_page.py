from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.wait_helpers import wait_present, wait_visible, wait_url_contains


class PIMPage(BasePage):
    LOC_PAGE_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")

    LOC_SEARCH_EMPLOYEE_ID = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']/../following-sibling::div//input",
    )
    LOC_SEARCH_EMPLOYEE_NAME = (
        By.XPATH,
        "//label[normalize-space()='Employee Name']/../following-sibling::div//input",
    )
    LOC_SEARCH_EMPLOYMENT_STATUS = (
        By.XPATH,
        "//label[normalize-space()='Employment Status']/../following-sibling::div//div[contains(@class,'oxd-select-text')]",
    )
    LOC_SEARCH_JOB_TITLE = (
        By.XPATH,
        "//label[normalize-space()='Job Title']/../following-sibling::div//div[contains(@class,'oxd-select-text')]",
    )
    LOC_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")

    LOC_ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    LOC_TABLE_ROWS = (By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[@role='row']")
    LOC_NO_RECORDS = (By.XPATH, "//*[normalize-space()='No Records Found']")
    LOC_DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='listbox']//span[normalize-space()]")
    LOC_FIRST_NAME = (By.XPATH, "//label[normalize-space()='First Name']/../following-sibling::div//input")
    LOC_FIRST_NAME_ALT = (
        By.XPATH,
        "//input[contains(@placeholder,'First Name') or @name='firstName' or @name='first_name']",
    )
    LOC_MIDDLE_NAME = (By.XPATH, "//label[normalize-space()='Middle Name']/../following-sibling::div//input")
    LOC_MIDDLE_NAME_ALT = (
        By.XPATH,
        "//input[contains(@placeholder,'Middle Name') or @name='middleName' or @name='middle_name']",
    )
    LOC_LAST_NAME = (By.XPATH, "//label[normalize-space()='Last Name']/../following-sibling::div//input")
    LOC_LAST_NAME_ALT = (
        By.XPATH,
        "//input[contains(@placeholder,'Last Name') or @name='lastName' or @name='last_name']",
    )
    LOC_EMPLOYEE_ID_FIELD = (By.XPATH, "//label[normalize-space()='Employee Id']/../following-sibling::div//input")
    LOC_EMPLOYEE_ID_FIELD_ALT = (
        By.XPATH,
        "//input[contains(@placeholder,'Employee Id') or @name='employeeId' or @name='employee_id']",
    )
    LOC_EMPLOYEE_ID_DISPLAY = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']/../following-sibling::div//span | //label[normalize-space()='Employee Id']/../following-sibling::div//div",
    )
    LOC_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")

    LOC_PERSONAL_DETAILS_TAB = (By.XPATH, "//a[normalize-space()='Personal Details'] | //h6[normalize-space()='Personal Details']")
    LOC_CONTACT_DETAILS_TAB = (By.XPATH, "//a[normalize-space()='Contact Details']")

    def get_header_text(self) -> str:
        return wait_visible(self.driver, *self.LOC_PAGE_HEADER, self.timeout).text.strip()

    def is_employee_list_loaded(self) -> bool:
        try:
            wait_url_contains(self.driver, "/pim", self.timeout)
            wait_visible(self.driver, *self.LOC_TABLE_ROWS, self.timeout)
            return True
        except Exception:
            return False

    def search_by_first_name(self, name: str) -> None:
        if self.is_visible(*self.LOC_SEARCH_EMPLOYEE_NAME):
            try:
                self.action_clear_and_type(*self.LOC_SEARCH_EMPLOYEE_NAME, name)
            except Exception:
                el = self.driver.find_element(*self.LOC_SEARCH_EMPLOYEE_NAME)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, name)
        else:
            elems = self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-form-row')]//input")
            if elems:
                try:
                    elems[0].clear()
                    elems[0].send_keys(name)
                except Exception:
                    self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", elems[0], name)
            else:
                try:
                    el = self.driver.find_element(*self.LOC_SEARCH_EMPLOYEE_NAME)
                    self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, name)
                except Exception:
                    raise

        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def search_by_employee_id(self, emp_id: str) -> None:
        try:
            self.driver.set_window_size(1920, 1080)
        except Exception:
            pass

        try:
            if not self.is_visible(*self.LOC_SEARCH_EMPLOYEE_ID):
                try:
                    toggle = self.driver.find_element(By.XPATH, "//div[contains(., 'Employee Information')]//button")
                    if toggle.is_displayed():
                        try:
                            toggle.click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", toggle)
                except Exception:
                    try:
                        alt = self.driver.find_element(By.XPATH, "//button[contains(@class,'oxd-icon-button')]")
                        if alt.is_displayed():
                            try:
                                alt.click()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", alt)
                    except Exception:
                        pass
        except Exception:
            pass

        if self.is_visible(*self.LOC_SEARCH_EMPLOYEE_ID):
            try:
                self.action_clear_and_type(*self.LOC_SEARCH_EMPLOYEE_ID, emp_id)
            except Exception:
                el = self.driver.find_element(*self.LOC_SEARCH_EMPLOYEE_ID)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, emp_id)
        else:
            elems = self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-form-row')]//input")
            target = None
            for e in elems:
                try:
                    t = e.get_attribute('type')
                    if t in ('text', 'tel'):
                        target = e
                        break
                except Exception:
                    continue

            if target:
                try:
                    target.clear()
                    target.send_keys(emp_id)
                except Exception:
                    self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", target, emp_id)
            else:
                el = self.driver.find_element(*self.LOC_SEARCH_EMPLOYEE_ID)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, emp_id)

        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def wait_for_search_results(self) -> None:
        def search_ready(driver):
            rows = driver.find_elements(*self.LOC_TABLE_ROWS)
            if any(row.text.strip() for row in rows):
                return True
            try:
                records = driver.find_elements(*self.LOC_NO_RECORDS)
                return any(node.is_displayed() for node in records)
            except Exception:
                return False

        WebDriverWait(self.driver, self.timeout).until(search_ready)

    def select_first_dropdown_option(self, dropdown_label_locator: tuple) -> str:
        try:
            self.action_click(*dropdown_label_locator)
        except Exception:
            # Fallback: try clicking via JS if the label element is covered or offscreen
            el = self.driver.find_element(*dropdown_label_locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", el)

        def option_list_ready(driver):
            items = driver.find_elements(*self.LOC_DROPDOWN_OPTIONS)
            return [item for item in items if item.is_displayed() and item.text.strip()]

        # Sometimes options render in an overlay container; attempt to expand waits
        try:
            options = WebDriverWait(self.driver, self.timeout).until(option_list_ready)
        except Exception:
            # Try a short JS-based wait to ensure overlay attached
            import time

            time.sleep(0.5)
            options = option_list_ready(self.driver)
        filtered = [opt for opt in options if opt.text.strip().lower() not in ("-- select --", "select", "please select", "- select -")]
        if not filtered:
            filtered = options
        if not filtered:
            raise ValueError("No dropdown options available")

        first_option = filtered[0]
        option_text = first_option.text.strip()
        try:
            first_option.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", first_option)

        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()
        return option_text

    def get_field_locator(self, primary: tuple, alternate: tuple) -> tuple:
        return primary if self.is_visible(*primary) else alternate

    def get_first_name_locator(self) -> tuple:
        return self.get_field_locator(self.LOC_FIRST_NAME, self.LOC_FIRST_NAME_ALT)

    def get_middle_name_locator(self) -> tuple:
        return self.get_field_locator(self.LOC_MIDDLE_NAME, self.LOC_MIDDLE_NAME_ALT)

    def get_last_name_locator(self) -> tuple:
        return self.get_field_locator(self.LOC_LAST_NAME, self.LOC_LAST_NAME_ALT)

    def get_employee_id_locator(self) -> tuple:
        return self.get_field_locator(self.LOC_EMPLOYEE_ID_FIELD, self.LOC_EMPLOYEE_ID_FIELD_ALT)

    def get_table_row_texts(self) -> list[str]:
        # Wait until either table rows are present (and contain text) or the
        # 'No Records Found' message is visible. This prevents timeouts when
        # the table is intentionally empty.
        def rows_or_no_records(driver):
            try:
                rows = driver.find_elements(*self.LOC_TABLE_ROWS)
                visible_rows = [r for r in rows if r.is_displayed() and r.text.strip()]
                if visible_rows:
                    return True
            except Exception:
                pass

            try:
                nodes = driver.find_elements(*self.LOC_NO_RECORDS)
                if any(n.is_displayed() for n in nodes):
                    return True
            except Exception:
                pass

            return False

        WebDriverWait(self.driver, self.timeout).until(rows_or_no_records)
        rows = self.driver.find_elements(*self.LOC_TABLE_ROWS)
        return [row.text.strip() for row in rows if row.is_displayed() and row.text.strip()]

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

        try:
            empty_nodes = self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[contains(normalize-space(.),'No Records') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'no records')]")
            if any(n.is_displayed() for n in empty_nodes):
                return True
        except Exception:
            pass

        return False

    def click_first_table_row(self) -> None:
        rows = self.driver.find_elements(*self.LOC_TABLE_ROWS)
        if not rows:
            raise ValueError("No employee rows found in table")

        first = rows[0]
        try:
            first.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", first)

    def action_open_add_employee(self) -> None:
        if self.is_visible(*self.LOC_FIRST_NAME) or self.is_visible(*self.LOC_FIRST_NAME_ALT):
            return

        try:
            try:
                self.action_click(*self.LOC_ADD_BUTTON)
            except Exception:
                btn = self.driver.find_element(*self.LOC_ADD_BUTTON)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", btn)

            if self.is_visible(*self.LOC_FIRST_NAME):
                return
            if self.is_visible(*self.LOC_FIRST_NAME_ALT):
                return

            wait_visible(self.driver, *self.LOC_FIRST_NAME, self.timeout)
            return
        except Exception:
            try:
                from urllib.parse import urlparse

                cur = urlparse(self.driver.current_url)
                base = f"{cur.scheme}://{cur.netloc}"
                self.driver.get(base + "/index.php/pim/addEmployee")
                if self.is_visible(*self.LOC_FIRST_NAME):
                    return
                wait_visible(self.driver, *self.LOC_FIRST_NAME_ALT, self.timeout)
                return
            except Exception:
                raise

    def add_employee(self, first_name: str, middle_name: str, last_name: str, employee_id: str | None = None) -> None:
        self.action_open_add_employee()
        self.action_clear_and_type(*self.get_first_name_locator(), first_name)
        
        if middle_name.strip():
            try:
                self.action_clear_and_type(*self.get_middle_name_locator(), middle_name)
            except Exception:
                pass
        
        self.action_clear_and_type(*self.get_last_name_locator(), last_name)
        
        if employee_id:
            self.action_clear_and_type(*self.get_employee_id_locator(), employee_id)
        
        # Dismiss any overlays before clicking save
        try:
            self.driver.execute_script("document.querySelectorAll('[role=\"dialog\"], .oxd-overlay').forEach(e => e.remove());")
        except Exception:
            pass
        
        self.action_click(*self.LOC_SAVE_BUTTON)
        import time
        import os
        from datetime import datetime

        def saved_or_details_ready(driver):
            try:
                if "addEmployee" not in driver.current_url:
                    return True
            except Exception:
                pass

            try:
                if driver.find_element(*self.LOC_PERSONAL_DETAILS_TAB).is_displayed():
                    return True
            except Exception:
                pass

            try:
                el = driver.find_element(*self.LOC_EMPLOYEE_ID_FIELD)
                if el and (el.get_attribute('value') or el.text):
                    return True
            except Exception:
                pass

            try:
                el2 = driver.find_element(*self.LOC_EMPLOYEE_ID_DISPLAY)
                if el2 and el2.text.strip():
                    return True
            except Exception:
                pass

            return False

        try:
            WebDriverWait(self.driver, max(30, self.timeout)).until(saved_or_details_ready)
        except Exception:
            # Save diagnostics
            try:
                reports_dir = os.path.join(os.getcwd(), "reports")
                os.makedirs(reports_dir, exist_ok=True)
                fname = os.path.join(reports_dir, f"add_employee_diagnostic_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.html")
                with open(fname, "w", encoding="utf-8") as fh:
                    fh.write(self.driver.page_source)
                print(f"ERROR: add_employee did not reach details view; saved page source to {fname}")
            except Exception:
                pass
            time.sleep(2)

    def get_current_employee_id(self) -> str:
        # Wait briefly for the employee id field or display to appear after save.
        try:
            try:
                wait_visible(self.driver, *self.LOC_EMPLOYEE_ID_FIELD, timeout=10)
                element = self.driver.find_element(*self.LOC_EMPLOYEE_ID_FIELD)
                val = element.get_attribute("value") or element.text or ""
                if val and val.strip():
                    return val.strip()
            except Exception:
                pass

            try:
                wait_visible(self.driver, *self.LOC_EMPLOYEE_ID_FIELD_ALT, timeout=5)
                element = self.driver.find_element(*self.LOC_EMPLOYEE_ID_FIELD_ALT)
                val = element.get_attribute("value") or element.text or ""
                if val and val.strip():
                    return val.strip()
            except Exception:
                pass

            try:
                wait_visible(self.driver, *self.LOC_EMPLOYEE_ID_DISPLAY, timeout=5)
                element = self.driver.find_element(*self.LOC_EMPLOYEE_ID_DISPLAY)
                val = element.text or ""
                if val and val.strip():
                    return val.strip()
            except Exception:
                pass
        except Exception:
            pass

        return ""

    def open_contact_details(self) -> None:
        self.action_click(*self.LOC_CONTACT_DETAILS_TAB)
        wait_visible(self.driver, *self.LOC_CONTACT_DETAILS_TAB, self.timeout)