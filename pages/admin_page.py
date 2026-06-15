from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.wait_helpers import wait_present, wait_visible, wait_url_contains


class AdminPage(BasePage):
    LOC_SYSTEM_USERS_HEADER = (
        By.XPATH,
        "//*[normalize-space()='System Users']",
    )
    LOC_USERNAME_FILTER = (
        By.XPATH,
        "//label[normalize-space()='Username']/../following-sibling::div//input | //input[@placeholder='Username' or contains(@placeholder,'Username')]",
    )
    LOC_USER_ROLE_FILTER = (
        By.XPATH,
        "//label[normalize-space()='User Role']/../following-sibling::div//div[contains(@class,'oxd-select-text')] | //div[contains(@class,'oxd-select-wrapper') and .//label[normalize-space()='User Role']]//div[contains(@class,'oxd-select-text')]",
    )
    LOC_STATUS_FILTER = (
        By.XPATH,
        "//label[normalize-space()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text')] | //div[contains(@class,'oxd-select-wrapper') and .//label[normalize-space()='Status']]//div[contains(@class,'oxd-select-text')]",
    )
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

    def search_username(self, username: str) -> None:
        # Wait for the username input to be visible before typing
        wait_visible(self.driver, *self.LOC_USERNAME_FILTER, self.timeout)
        self.action_clear_and_type(*self.LOC_USERNAME_FILTER, username)
        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def filter_user_role(self, role: str) -> None:
        # Wait for the User Role dropdown to be visible before clicking
        wait_visible(self.driver, *self.LOC_USER_ROLE_FILTER, self.timeout)
        self.action_click(*self.LOC_USER_ROLE_FILTER)
        # Wait for listbox options to appear
        wait_present(self.driver, By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{role}']", self.timeout)
        self.action_click(By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{role}']")
        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def filter_status(self, status: str) -> None:
        # Wait for the Status dropdown to be visible before clicking
        wait_visible(self.driver, *self.LOC_STATUS_FILTER, self.timeout)
        self.action_click(*self.LOC_STATUS_FILTER)
        # Wait for listbox options to appear
        wait_present(self.driver, By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{status}']", self.timeout)
        self.action_click(By.XPATH, f"//div[@role='listbox']//span[normalize-space()='{status}']")
        self.action_click(*self.LOC_SEARCH_BUTTON)
        self.wait_for_search_results()

    def get_table_row_texts(self) -> list[str]:
        try:
            wait_present(self.driver, *self.LOC_TABLE_ROWS, self.timeout)
        except Exception:
            return []
        rows = self.driver.find_elements(*self.LOC_TABLE_ROWS)
        return [row.text.strip() for row in rows if row.is_displayed() and row.text.strip()]

    def is_no_records_found_visible(self) -> bool:
        try:
            return self.is_visible(*self.LOC_NO_RECORDS)
        except Exception:
            return False

    def wait_for_search_results(self) -> None:
        def search_ready(driver):
            rows = driver.find_elements(*self.LOC_TABLE_ROWS)
            if any(row.is_displayed() and row.text.strip() for row in rows):
                return True
            try:
                no_records = driver.find_elements(*self.LOC_NO_RECORDS)
                return any(node.is_displayed() for node in no_records)
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