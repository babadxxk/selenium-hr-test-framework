from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)

from pages.base_page import BasePage
from utils.wait_helpers import wait_present, wait_visible, wait_url_contains


class AdminPage(BasePage):
    LOC_SYSTEM_USERS_HEADER = (
        By.XPATH,
        "//*[normalize-space()='System Users']",
    )
    LOC_FILTER_TOGGLE = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-filter-header-options')]//button[contains(@class,'oxd-icon-button')]",
    )
    LOC_USERNAME_FILTER = (
        By.XPATH,
        "//label[normalize-space()='Username']/../following-sibling::div//input | //input[@placeholder='Username' or contains(@placeholder,'Username')]",
    )
    # user role / status filters removed (requirements FR-ADM-03 & FR-ADM-04)
    LOC_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    LOC_ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    LOC_TABLE_ROWS = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-body')]//div[@role='row'] | //div[contains(@class,'oxd-table-card')]",
    )
    LOC_NO_RECORDS = (By.XPATH, "//*[normalize-space()='No Records Found']")
    LOC_ADD_USER_HEADER = (By.XPATH, "//h6[normalize-space()='Add User']")
    LOC_ADD_USER_ROLE = (
        By.XPATH,
        "//label[normalize-space()='User Role']/../following-sibling::div//div[contains(@class,'oxd-select-text')] | //div[contains(@class,'oxd-form-row')]//label[normalize-space()='User Role']/following::div[contains(@class,'oxd-select-text')][1]",
    )
    LOC_ADD_EMPLOYEE_NAME = (
        By.XPATH,
        "//label[normalize-space()='Employee Name']/../following-sibling::div//input | //input[@placeholder='Type for hints...']",
    )
    LOC_ADD_STATUS = (
        By.XPATH,
        "//label[normalize-space()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text')] | //div[contains(@class,'oxd-form-row')]//label[normalize-space()='Status']/following::div[contains(@class,'oxd-select-text')][1]",
    )
    LOC_ADD_USERNAME = (
        By.XPATH,
        "//label[normalize-space()='Username']/../following-sibling::div//input | //input[@placeholder='Username' or @name='username']",
    )
    LOC_ADD_PASSWORD = (
        By.XPATH,
        "//label[normalize-space()='Password']/../following-sibling::div//input | //input[@type='password' and contains(@name,'password')][1]",
    )
    LOC_ADD_CONFIRM_PASSWORD = (
        By.XPATH,
        "//label[normalize-space()='Confirm Password']/../following-sibling::div//input | //input[@type='password' and contains(@name,'confirm')]",
    )

    def is_system_users_loaded(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_SYSTEM_USERS_HEADER, self.timeout)
            return True
        except Exception:
            return False

    def _find_element_resilient(self, by, locator):
        """Try visibility wait first, then fall back to presence + scroll.

        Returns the WebElement or raises the original exception.
        """
        try:
            el = wait_visible(self.driver, by, locator, self.timeout)
            if el.is_displayed() and el.is_enabled():
                return el
        except Exception:
            pass

        # fallback: look for any present matching element that is displayed+enabled
        try:
            candidates = self.driver.find_elements(by, locator)
            for el in candidates:
                if el.is_displayed() and el.is_enabled():
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    except Exception:
                        pass
                    return el
        except Exception:
            pass

        # final fallback: presence wait + return whatever it finds (will raise if not found)
        # If filter controls are collapsed, try toggling the filter panel and retry
        try:
            self.action_click(*self.LOC_FILTER_TOGGLE)
            try:
                el = wait_visible(self.driver, by, locator, 3)
                if el.is_displayed() and el.is_enabled():
                    return el
            except Exception:
                pass
        except Exception:
            pass

        return wait_present(self.driver, by, locator, self.timeout)

    def _wait_for_option(self, texts: list[str]) -> tuple[bool, object]:
        """Wait for any of the provided XPaths/texts to be present and return the locator tuple.

        Returns (found, (By, locator))
        """
        # removed helper for option-waiting (filter option selection removed)
        return False, (By.XPATH, "")

    def search_username(self, username: str) -> None:
        # Try using the action helper first (handles clickable visibility)
        try:
            self.action_clear_and_type(*self.LOC_USERNAME_FILTER, username)
        except (TimeoutException, ElementNotInteractableException):
            # fallback: find a displayed+enabled input and set value via JS
            try:
                el = self._find_element_resilient(*self.LOC_USERNAME_FILTER)
                try:
                    el.clear()
                    el.send_keys(username)
                except Exception:
                    # last resort: set value via JS and dispatch input event
                    self.driver.execute_script(
                        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
                        el,
                        username,
                    )
            except Exception:
                # if all fails, re-raise so test sees the failure
                raise
        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    # filter methods removed (requirements FR-ADM-03 & FR-ADM-04)

    def get_table_row_texts(self) -> list[str]:
        try:
            # wait for at least one row or card to be present
            wait_present(self.driver, *self.LOC_TABLE_ROWS, self.timeout)
        except Exception:
            return []

        results: list[str] = []
        seen: set[str] = set()

        # Prefer structured rows with role='row'
        try:
            rows = self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[@role='row']")
            for r in rows:
                try:
                    if not r.is_displayed():
                        continue
                    text = r.text.strip()
                    if text and text not in seen:
                        results.append(text)
                        seen.add(text)
                except Exception:
                    continue
        except Exception:
            pass

        # Also include top-level card elements if present
        try:
            cards = self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-card') and not(ancestor::div[contains(@class,'oxd-table-card')])]")
            for c in cards:
                try:
                    if not c.is_displayed():
                        continue
                    text = c.text.strip()
                    if text and text not in seen:
                        results.append(text)
                        seen.add(text)
                except Exception:
                    continue
        except Exception:
            pass

        # Fallback: use the original locator if nothing found
        if not results:
            try:
                rows = self.driver.find_elements(*self.LOC_TABLE_ROWS)
                for row in rows:
                    try:
                        if not row.is_displayed():
                            continue
                        text = row.text.strip()
                        if text and text not in seen:
                            results.append(text)
                            seen.add(text)
                    except Exception:
                        continue
            except Exception:
                return []

        return results

    def is_no_records_found_visible(self) -> bool:
        try:
            return self.is_visible(*self.LOC_NO_RECORDS)
        except Exception:
            return False

    def wait_for_search_results(self) -> None:
        def search_ready(driver):
            try:
                rows = driver.find_elements(*self.LOC_TABLE_ROWS)
                for row in rows:
                    try:
                        if row.is_displayed() and row.text.strip():
                            return True
                    except StaleElementReferenceException:
                        # element became stale; try next one
                        continue

                try:
                    no_records = driver.find_elements(*self.LOC_NO_RECORDS)
                    for node in no_records:
                        try:
                            if node.is_displayed():
                                return True
                        except StaleElementReferenceException:
                            continue
                    return False
                except Exception:
                    return False
            except Exception:
                return False

        WebDriverWait(self.driver, self.timeout).until(search_ready)

    def open_add_user_form(self) -> None:
        self.action_click(*self.LOC_ADD_BUTTON)
        wait_visible(self.driver, *self.LOC_ADD_USER_HEADER, self.timeout)

    def is_add_user_form_loaded(self) -> bool:
        fields = [
            self.LOC_ADD_USER_HEADER,
            self.LOC_ADD_USER_ROLE,
            self.LOC_ADD_EMPLOYEE_NAME,
            self.LOC_ADD_STATUS,
            self.LOC_ADD_USERNAME,
            self.LOC_ADD_PASSWORD,
            self.LOC_ADD_CONFIRM_PASSWORD,
        ]
        return all(self.is_visible(*field) for field in fields)

    def submit_add_user_form(
        self,
        user_role: str | None = None,
        employee_name: str | None = None,
        status: str | None = None,
        username: str | None = None,
        password: str | None = None,
        confirm_password: str | None = None,
    ) -> None:
        if user_role:
            self.action_click(*self.LOC_ADD_USER_ROLE)
            self.action_click(By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{user_role}']")
        if employee_name:
            self.action_clear_and_type(*self.LOC_ADD_EMPLOYEE_NAME, employee_name)
        if status:
            self.action_click(*self.LOC_ADD_STATUS)
            self.action_click(By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{status}']")
        if username is not None:
            self.action_clear_and_type(*self.LOC_ADD_USERNAME, username)
        if password is not None:
            self.action_clear_and_type(*self.LOC_ADD_PASSWORD, password)
        if confirm_password is not None:
            self.action_clear_and_type(*self.LOC_ADD_CONFIRM_PASSWORD, confirm_password)

        self.action_click_button("Save")

    def get_add_user_validation_messages(self) -> list[str]:
        return self.get_required_error_messages()