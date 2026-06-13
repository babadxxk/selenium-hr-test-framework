from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.wait_helpers import wait_url_contains


class LoginPage(BasePage):
    LOC_USERNAME = (By.NAME, "username")
    LOC_PASSWORD = (By.NAME, "password")
    LOC_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOC_ERROR = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    LOC_USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")

    def action_login(self, username: str, password: str) -> None:
        self.action_type(*self.LOC_USERNAME, username)
        self.action_type(*self.LOC_PASSWORD, password)
        self.action_click(*self.LOC_LOGIN_BUTTON)

    def action_submit_login_form(self) -> None:
        self.action_click(*self.LOC_LOGIN_BUTTON)

    def is_state_logged_in(self) -> bool:
        try:
            wait_url_contains(self.driver, "/dashboard", self.timeout)
            return True
        except Exception:
            return False

    def is_state_on_login_page(self) -> bool:
        return "/auth/login" in self.driver.current_url

    def is_user_dropdown_visible(self) -> bool:
        return self.is_visible(*self.LOC_USER_DROPDOWN)

    def get_error_message(self) -> str:
        return self.get_text(*self.LOC_ERROR)

    def get_required_error_count(self) -> int:
        return len(self.driver.find_elements(*self.LOC_REQUIRED_ERRORS))