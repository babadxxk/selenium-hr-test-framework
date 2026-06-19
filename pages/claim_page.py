from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.wait_helpers import wait_visible, wait_url_contains


class ClaimPage(BasePage):
    LOC_SUBMIT_TAB = (By.XPATH, "//a[normalize-space()='Submit Claim'] | //button[normalize-space()='Submit Claim']")

    LOC_EVENT_DROPDOWN = (By.XPATH, "//label[contains(normalize-space(),'Event')]/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
    LOC_DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='listbox']//span[normalize-space()]")
    LOC_EVENT_DROPDOWN_ALT = (By.XPATH, "//label[contains(.,'Event')]/ancestor::div[1]//div[contains(@class,'oxd-select-text')] | //div[contains(@class,'oxd-form-row')]//label[contains(.,'Event')]/following::div[contains(@class,'oxd-select-text')][1]")
    LOC_CURRENCY_FIELD = (By.XPATH, "//label[contains(normalize-space(),'Currency')]/../following-sibling::div//div[contains(@class,'oxd-select-text')] | //select[@name='currency']")
    LOC_DATE_FIELD = (By.XPATH, "//label[contains(normalize-space(),'Date')]/../following-sibling::div//input | //input[@name='date'] | //label[contains(.,'Date')]/ancestor::div//input[contains(@class,'oxd-input')]")
    LOC_REMARKS_FIELD = (By.XPATH, "//label[contains(normalize-space(),'Remarks')]/../following-sibling::div//textarea | //textarea[@name='comment']")
    LOC_SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit'] | //button[contains(., 'Submit')]" )

    LOC_EVENTS_TAB = (By.XPATH, "//a[normalize-space()='Events'] | //button[normalize-space()='Events'] | //a[contains(., 'Events')]")
    LOC_EVENTS_TABLE = (By.XPATH, "//table[@role='table'] | //div[contains(@class,'oxd-table')]")
    LOC_ADD_EVENT_BUTTON = (By.XPATH, "//button[normalize-space()='Add'] | //button[contains(., 'Add')]")
    LOC_EVENT_NAME_INPUT = (By.XPATH, "//label[normalize-space()='Event Name']/../following-sibling::div//input | //input[contains(@name,'event') or contains(@placeholder,'Event')]")
    LOC_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save'] | //button[contains(., 'Save')]")

    LOC_EMPLOYEE_CLAIMS_TAB = (By.XPATH, "//a[normalize-space()='Employee Claims'] | //button[normalize-space()='Employee Claims'] | //a[contains(., 'Employee Claims')]")
    LOC_RECORDS_TABLE = (By.XPATH, "//table[@role='table' and (./thead or .//th)] | //div[contains(@class,'oxd-table')]")

    def go_to_submit_claim(self) -> None:
        # Open the Submit Claim tab or ensure claim section is loaded
        try:
            self.action_click(*self.LOC_SUBMIT_TAB)
        except Exception:
            wait_url_contains(self.driver, "/claim", self.timeout)

    def is_submit_claim_loaded(self) -> bool:
        # Verify Submit Claim form fields are present
        try:
            try:
                self.action_dismiss_blocking_overlays()
            except Exception:
                pass
            try:
                wait_visible(self.driver, *self.LOC_EVENT_DROPDOWN, self.timeout)
            except Exception:
                wait_visible(self.driver, *self.LOC_EVENT_DROPDOWN_ALT, max(3, self.timeout))
            wait_visible(self.driver, *self.LOC_CURRENCY_FIELD, self.timeout)
            wait_visible(self.driver, *self.LOC_DATE_FIELD, self.timeout)
            wait_visible(self.driver, *self.LOC_REMARKS_FIELD, self.timeout)
            return True
        except Exception:
            return False

    def get_event_options(self) -> list[str]:
        # Open the Event dropdown and return available option texts
        clicked = False
        try:
            self.action_click(*self.LOC_EVENT_DROPDOWN)
            clicked = True
        except Exception:
            try:
                self.action_click(*self.LOC_EVENT_DROPDOWN_ALT)
                clicked = True
            except Exception:
                try:
                    el = self.driver.find_element(*self.LOC_EVENT_DROPDOWN)
                    self.driver.execute_script("arguments[0].click();", el)
                    clicked = True
                except Exception:
                    pass
        if not clicked:
            return []
        try:
            WebDriverWait(self.driver, 5).until(lambda d: d.find_elements(*self.LOC_DROPDOWN_OPTIONS))
            opts = [o.text.strip() for o in self.driver.find_elements(*self.LOC_DROPDOWN_OPTIONS) if o.text.strip()]
            return opts
        except Exception:
            return []

    def is_event_dropdown_present(self) -> bool:
        """Return True if an Event dropdown element is present in the Submit Claim form."""
        try:
            if self.driver.find_elements(*self.LOC_EVENT_DROPDOWN):
                return True
            if self.driver.find_elements(*self.LOC_EVENT_DROPDOWN_ALT):
                return True
            return False
        except Exception:
            return False

    def submit_claim_without_event(self) -> None:
        # Attempt to submit the form without selecting an event to trigger required validation
        try:
            self.action_click(*self.LOC_SUBMIT_BUTTON)
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_SUBMIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass
        try:
            wait_visible(self.driver, *self.LOC_REQUIRED_ERRORS, 3)
        except Exception:
            try:
                wait_visible(self.driver, By.XPATH, "//*[contains(normalize-space(.),'Required') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'required') ]", 3)
            except Exception:
                pass

    def is_required_error_visible(self) -> bool:
        try:
            if self.get_required_error_count() > 0:
                return True
        except Exception:
            pass
        try:
            el = self.driver.find_element(By.XPATH, "//*[contains(normalize-space(.),'Required') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'required')]")
            return bool(el and el.text.strip())
        except Exception:
            return False
    def go_to_events_config(self) -> None:
        try:
            cfg = (By.XPATH, "//button[normalize-space()='Configuration'] | //div[contains(@class,'oxd-topbar-body')]//button[contains(., 'Configuration')]")
            try:
                self.action_click(*cfg)
            except Exception:
                pass

            self.action_click(*self.LOC_EVENTS_TAB)
        except Exception:
            base = self.driver.current_url.split('/web')[0]
            candidates = [
                "/web/index.php/claim/configureClaim",
                "/web/index.php/claim/saveClaimEvent",
                "/web/index.php/claim/listClaimEvent",
                "/web/index.php/claim/listClaimEvents",
            ]
            for path in candidates:
                try:
                    self.driver.get(base + path)
                    break
                except Exception:
                    continue

        wait_url_contains(self.driver, "claim", self.timeout)
        try:
            wait_visible(self.driver, *self.LOC_EVENTS_TABLE, self.timeout)
        except Exception:
            pass

    def is_events_list_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_EVENTS_TABLE, self.timeout)
            return True
        except Exception:
            return False

    def add_event(self, name: str | None) -> None:
        # Add an Event entry (or click Save without name if None)
        try:
            self.action_click(*self.LOC_ADD_EVENT_BUTTON)
        except Exception:
            pass
        if name is None:
            try:
                self.action_click(*self.LOC_SAVE_BUTTON)
            except Exception:
                pass
            return
        try:
            self.action_clear_and_type(*self.LOC_EVENT_NAME_INPUT, name)
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_EVENT_NAME_INPUT)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, name)
            except Exception:
                pass
        try:
            self.action_click(*self.LOC_SAVE_BUTTON)
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_SAVE_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass

    def get_events_texts(self) -> list[str]:
        # Return texts of existing events from the events table
        try:
            rows = self.driver.find_elements(By.XPATH, "//table//tbody//tr | //div[contains(@class,'oxd-table')]//div[contains(@class,'oxd-table-row')]")
            return [r.text.strip() for r in rows if r.text.strip()]
        except Exception:
            return []

    def go_to_employee_claims(self) -> None:
        """Navigate to the Employee Claims tab and wait for the records table to appear."""
        try:
            self.action_click(*self.LOC_EMPLOYEE_CLAIMS_TAB)
        except Exception:
            base = self.driver.current_url.split('/web')[0]
            candidates = [
                "/web/index.php/claim/viewClaimList",
                "/web/index.php/claim/employeeClaims",
                "/web/index.php/claim/listClaim",
            ]
            for path in candidates:
                try:
                    self.driver.get(base + path)
                    break
                except Exception:
                    continue

        try:
            wait_visible(self.driver, *self.LOC_RECORDS_TABLE, self.timeout)
        except Exception:
            pass

    def is_records_table_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_RECORDS_TABLE, self.timeout)
            return True
        except Exception:
            return False
