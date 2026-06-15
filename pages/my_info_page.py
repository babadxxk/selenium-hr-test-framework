from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.wait_helpers import wait_visible, wait_present


class MyInfoPage(BasePage):
    LOC_PERSONAL_TAB = (By.XPATH, "//a[normalize-space()='Personal Details'] | //h6[normalize-space()='Personal Details']")
    LOC_CONTACT_TAB = (By.XPATH, "//a[normalize-space()='Contact Details']")
    LOC_DEPENDANTS_TAB = (By.XPATH, "//a[normalize-space()='Dependents'] | //a[normalize-space()='Dependants']")
    LOC_IMMIGRATION_TAB = (By.XPATH, "//a[normalize-space()='Immigration']")
    LOC_QUALIFICATIONS_TAB = (By.XPATH, "//a[normalize-space()='Qualifications']")

    # Personal details fields (flexible: input or span)
    LOC_FULLNAME = (By.XPATH, "//h6[contains(@class,'oxd-text')][1] | //label[normalize-space()='Full Name']/../following-sibling::div//span")
    LOC_EMPLOYEE_ID = (By.XPATH, "//label[normalize-space()='Employee Id']/../following-sibling::div//span | //label[normalize-space()='Employee Id']/../following-sibling::div//input")
    LOC_DOB = (By.XPATH, "//label[contains(normalize-space(),'Date of Birth')]/../following-sibling::div//input | //label[contains(normalize-space(),'Date of Birth')]/../following-sibling::div//span")
    LOC_GENDER = (By.XPATH, "//label[normalize-space()='Gender']/../following-sibling::div//span | //label[normalize-space()='Gender']/../following-sibling::div//input")
    LOC_NATIONALITY = (By.XPATH, "//label[normalize-space()='Nationality']/../following-sibling::div//span | //label[normalize-space()='Nationality']/../following-sibling::div//input")
    LOC_MARITAL_STATUS = (By.XPATH, "//label[normalize-space()='Marital Status']/../following-sibling::div//span | //label[normalize-space()='Marital Status']/../following-sibling::div//input")
    LOC_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")

    # Contact details
    LOC_ADDRESS = (By.XPATH, "//label[contains(normalize-space(),'Address')]/../following-sibling::div//textarea | //label[contains(normalize-space(),'Address')]/../following-sibling::div//input")
    LOC_TELEPHONE = (By.XPATH, "//label[contains(normalize-space(),'Telephone')]/../following-sibling::div//input")
    LOC_MOBILE = (By.XPATH, "//label[contains(normalize-space(),'Mobile')]/../following-sibling::div//input")
    LOC_WORK_EMAIL = (By.XPATH, "//label[contains(normalize-space(),'Work Email')]/../following-sibling::div//input | //label[contains(normalize-space(),'Work Email')]/../following-sibling::div//span")

    # Dependents
    LOC_DEPENDANTS_ADD = (By.XPATH, "//button[normalize-space()='Add'] | //a[normalize-space()='Add']")

    # Immigration (generic check)
    LOC_IMMIGRATION_HEADER = (By.XPATH, "//h6[normalize-space()='Immigration'] | //h3[normalize-space()='Immigration']")

    # Qualifications -> Work Experience
    LOC_QUALIFICATIONS_SECTION = (By.XPATH, "//h6[normalize-space()='Qualifications'] | //a[normalize-space()='Qualifications']")
    LOC_WORK_EXPERIENCE_ADD = (By.XPATH, "//button[contains(normalize-space(),'Add') and contains(., 'Work')] | //section//button[normalize-space()='Add']")
    LOC_WORK_COMPANY = (By.XPATH, "//label[contains(normalize-space(),'Company')]/../following-sibling::div//input")
    LOC_WORK_TITLE = (By.XPATH, "//label[contains(normalize-space(),'Job Title')]/../following-sibling::div//input")
    LOC_WORK_FROM = (By.XPATH, "//label[contains(normalize-space(),'From')]/../following-sibling::div//input")
    LOC_WORK_TO = (By.XPATH, "//label[contains(normalize-space(),'To')]/../following-sibling::div//input")
    LOC_WORK_SAVE = (By.XPATH, "//button[normalize-space()='Save'] | //button[normalize-space()='Add']")
    LOC_WORK_ROWS = (By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[@role='row']")

    def is_personal_details_loaded(self) -> bool:
        try:
            wait_present(self.driver, *self.LOC_FULLNAME, self.timeout)
            # check key fields
            fields = [self.LOC_EMPLOYEE_ID, self.LOC_DOB, self.LOC_GENDER, self.LOC_NATIONALITY, self.LOC_MARITAL_STATUS]
            for f in fields:
                if not self.is_visible(*f):
                    return False
            return True
        except Exception:
            return False

    def open_contact_details(self) -> None:
        self.action_click(*self.LOC_CONTACT_TAB)
        wait_visible(self.driver, *self.LOC_WORK_EMAIL, self.timeout)

    def set_work_email_and_save(self, email: str) -> None:
        try:
            self.action_clear_and_type(*self.LOC_WORK_EMAIL, email)
            # trigger blur to activate validation
            el = self.driver.find_element(*self.LOC_WORK_EMAIL)
            el.send_keys('\t')
            self.action_click(*self.LOC_SAVE_BUTTON)
        except Exception:
            raise

    def wait_for_validation_errors(self, timeout: int = 5) -> int:
        import time

        end = time.time() + timeout
        while time.time() < end:
            count = self.get_required_error_count()
            if count > 0:
                return count
            time.sleep(0.5)
        return 0

    def open_dependants_tab(self) -> None:
        self.action_click(*self.LOC_DEPENDANTS_TAB)

    def has_dependants_add(self) -> bool:
        try:
            return self.is_visible(*self.LOC_DEPENDANTS_ADD)
        except Exception:
            return False

    def open_immigration_tab(self) -> None:
        self.action_click(*self.LOC_IMMIGRATION_TAB)

    def has_immigration_fields(self) -> bool:
        try:
            if self.is_visible(*self.LOC_IMMIGRATION_HEADER):
                return True
            # alternative checks: passport/number labels or table rows under immigration
            alt = (
                By.XPATH,
                "//label[contains(normalize-space(),'Passport')]|//label[contains(normalize-space(),'Immigration')]|//h6[contains(normalize-space(),'Immigration Records')]",
            )
            return self.is_visible(*alt)
        except Exception:
            return False

    def open_qualifications_tab(self) -> None:
        self.action_click(*self.LOC_QUALIFICATIONS_TAB)

    def add_work_experience(self, company: str, title: str, frm: str, to: str) -> None:
        try:
            # Try clicking the Add button scoped to Work Experience
            try:
                header_add = (
                    By.XPATH,
                    "//h6[normalize-space()='Work Experience']/following::button[normalize-space()='Add'][1]",
                )
                self.action_click(*header_add)
            except Exception:
                try:
                    self.action_click(*self.LOC_WORK_EXPERIENCE_ADD)
                except Exception:
                    # fallback: click any Add button
                    self.action_click(*self.LOC_WORK_SAVE)

            # Wait for fields to appear (company/title)
            try:
                wait_present(self.driver, *self.LOC_WORK_COMPANY, self.timeout)
            except Exception:
                pass

            self.action_clear_and_type(*self.LOC_WORK_COMPANY, company)
            self.action_clear_and_type(*self.LOC_WORK_TITLE, title)
            self.action_clear_and_type(*self.LOC_WORK_FROM, frm)
            self.action_clear_and_type(*self.LOC_WORK_TO, to)
            self.action_click(*self.LOC_WORK_SAVE)
            # small wait for save to complete
            import time

            time.sleep(1)
        except Exception:
            raise

    def get_work_experience_rows(self) -> list[str]:
        try:
            wait_present(self.driver, *self.LOC_WORK_ROWS, self.timeout)
        except Exception:
            return []
        rows = self.driver.find_elements(*self.LOC_WORK_ROWS)
        return [r.text.strip() for r in rows if r.is_displayed() and r.text.strip()]
