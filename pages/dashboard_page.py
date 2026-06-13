from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.wait_helpers import wait_url_contains, wait_visible

class DashboardPage(BasePage):
    LOC_USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOC_LOGOUT = (By.XPATH, "//a[normalize-space()='Logout']")
    LOC_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    LOC_WIDGETS = (By.CSS_SELECTOR, ".orangehrm-dashboard-widget")
    
    def is_state_on_dashboard(self) -> bool:
        """Check if user is on dashboard by verifying user dropdown is visible."""
        return self.is_visible(*self.LOC_USER_DROPDOWN)
    
    def is_user_dropdown_visible(self) -> bool:
        """Verify user dropdown is visible in the top-right corner."""
        return self.is_visible(*self.LOC_USER_DROPDOWN)
    
    def get_visible_widgets_count(self) -> int:
        """Get count of visible dashboard widgets."""
        wait_url_contains(self.driver, "/dashboard", self.timeout)
        return len(self.driver.find_elements(*self.LOC_WIDGETS))
    
    def action_logout(self) -> None:
        """Perform logout action."""
        self.action_click(*self.LOC_USER_DROPDOWN)
        self.action_click(*self.LOC_LOGOUT)
        wait_url_contains(self.driver, "/auth/login", self.timeout)
    
    def action_refresh_dashboard(self) -> None:
        """Refresh the dashboard page."""
        self.driver.refresh()
        # Wait for dashboard to load after refresh
        wait_url_contains(self.driver, "/dashboard", self.timeout)
        
    def get_header_text(self) -> str:
        """Get the header text from the dashboard."""
        return wait_visible(self.driver, *self.LOC_HEADER, self.timeout).text.strip()