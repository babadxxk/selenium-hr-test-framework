from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from utils.wait_helpers import wait_visible, wait_url_contains


class MaintenancePage(BasePage):
    LOC_PASSWORD_MODAL = (
        By.XPATH,
        "//div[contains(@class,'oxd-dialog-container') or contains(.,'Admin Access') or //label[contains(normalize-space(),'Password')]]",
    )
    LOC_PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or contains(@placeholder,'Password')]")
    LOC_PASSWORD_CONFIRM = (By.XPATH, "//button[normalize-space()='Confirm'] | //button[normalize-space()='Submit'] | //button[contains(.,'Confirm')]")
    LOC_INVALID_CREDENTIALS = (By.XPATH, "//*[contains(normalize-space(),'Invalid') or contains(normalize-space(),'invalid') or contains(.,'Invalid credentials')]")

    LOC_MAINTENANCE_HEADER = (
        By.XPATH,
        "//h6[contains(normalize-space(),'Purge Employee Records') or contains(normalize-space(),'Maintenance') or contains(normalize-space(),'Purge')]")

    LOC_ACCESS_RECORDS_TAB = (By.XPATH, "//a[normalize-space()='Access Records'] | //button[normalize-space()='Access Records']")
    LOC_ACCESS_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...' or contains(@placeholder,'Type for hints')]")
    LOC_ACCESS_RESULTS_ROWS = (By.XPATH, "//table//tbody//tr | //div[contains(@class,'oxd-table')]//div[contains(@class,'oxd-table-row')]")

    def is_password_prompt_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_PASSWORD_MODAL, 5)
            return True
        except Exception:
            return False

    def submit_password(self, password: str) -> None:
        try:
            self.action_clear_and_type(*self.LOC_PASSWORD_INPUT, password)
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_PASSWORD_INPUT)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, password)
            except Exception:
                pass
        try:
            self.action_click(*self.LOC_PASSWORD_CONFIRM)
        except Exception:
            pass

    def is_maintenance_landing_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_MAINTENANCE_HEADER, self.timeout)
            return True
        except Exception:
            return False

    def is_invalid_credentials_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_INVALID_CREDENTIALS, 3)
            return True
        except Exception:
            return False

    def go_to_access_records(self) -> None:
        try:
            self.action_click(*self.LOC_ACCESS_RECORDS_TAB)
        except Exception:
            # try via URL fragment
            base = self.driver.current_url.split('/web')[0]
            url = base + "/web/index.php/maintenance/viewPurgeEmployee"
            self.driver.get(url)

        # wait for the maintenance context and the access records search input to be visible
        wait_url_contains(self.driver, "maintenance", self.timeout)
        try:
            wait_visible(self.driver, *self.LOC_ACCESS_SEARCH_INPUT, self.timeout)
        except Exception:
            # tolerate absence but continue
            pass

    def search_access_records(self, name: str) -> None:
        try:
            self.action_clear_and_type(*self.LOC_ACCESS_SEARCH_INPUT, name)
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_ACCESS_SEARCH_INPUT)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, name)
            except Exception:
                pass
        try:
            # try pressing Enter
            el = self.driver.find_element(*self.LOC_ACCESS_SEARCH_INPUT)
            el.send_keys('\n')
        except Exception:
            try:
                self.action_click(*self.LOC_PASSWORD_CONFIRM)
            except Exception:
                pass

        # wait for either results rows or a 'No Records' indicator
        def results_ready(driver):
            try:
                if driver.find_elements(*self.LOC_ACCESS_RESULTS_ROWS):
                    return True
            except Exception:
                pass
            try:
                no_rec = driver.find_elements(By.XPATH, "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'no records')]")
                if no_rec:
                    return True
            except Exception:
                pass
            return False

        try:
            WebDriverWait(self.driver, self.timeout).until(results_ready)
        except Exception:
            pass

    def get_access_result_texts(self) -> list[str]:
        try:
            rows = self.driver.find_elements(*self.LOC_ACCESS_RESULTS_ROWS)
            texts = [r.text.strip() for r in rows if r.text.strip()]
            return texts
        except Exception:
            return []
