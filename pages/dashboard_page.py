from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.wait_helpers import wait_present, wait_url_contains, wait_visible


class DashboardPage(BasePage):
    LOC_USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOC_LOGOUT = (By.XPATH, "//a[normalize-space()='Logout']")
    LOC_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    LOC_WIDGETS = (By.CSS_SELECTOR, ".orangehrm-dashboard-widget")

    LOC_TIME_AT_WORK = (By.XPATH, "//*[normalize-space()='Time at Work']")
    LOC_MY_ACTIONS = (By.XPATH, "//*[normalize-space()='My Actions']")
    LOC_QUICK_LAUNCH = (By.XPATH, "//*[normalize-space()='Quick Launch']")
    LOC_EMPLOYEE_DISTRIBUTION_SUB_UNIT = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Employee Distribution by Sub Unit')]",
    )
    LOC_EMPLOYEE_DISTRIBUTION_LOCATION = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Employee Distribution by Location')]",
    )

    LOC_ASSIGN_LEAVE = (By.XPATH, "//*[normalize-space()='Assign Leave']")
    LOC_LEAVE_LIST = (By.XPATH, "//*[normalize-space()='Leave List']")
    LOC_TIMESHEETS = (By.XPATH, "//*[normalize-space()='Timesheets']")
    LOC_APPLY_LEAVE = (By.XPATH, "//*[normalize-space()='Apply Leave']")
    LOC_MY_LEAVE = (By.XPATH, "//*[normalize-space()='My Leave']")
    LOC_MY_TIMESHEET = (By.XPATH, "//*[normalize-space()='My Timesheet']")

    LOC_ADMIN_MENU = (
        By.XPATH,
        "//a[contains(@href, '/admin/viewAdminModule') or normalize-space()='Admin']",
    )
    LOC_PIM_MENU = (
        By.XPATH,
        "//a[contains(@href, '/pim/viewPimModule') or normalize-space()='PIM']",
    )
    LOC_LEAVE_MENU = (
        By.XPATH,
        "//a[contains(@href, '/leave/viewLeaveModule') or normalize-space()='Leave']",
    )
    LOC_TIME_MENU = (
        By.XPATH,
        "//a[contains(@href, '/time/viewTimeModule') or normalize-space()='Time']",
    )
    LOC_RECRUITMENT_MENU = (
        By.XPATH,
        "//a[contains(@href, '/recruitment/viewRecruitmentModule') or normalize-space()='Recruitment']",
    )
    LOC_MY_INFO_MENU = (
        By.XPATH,
        "//a[contains(@href, '/pim/viewMyDetails') or normalize-space()='My Info']",
    )
    LOC_PERFORMANCE_MENU = (
        By.XPATH,
        "//a[contains(@href, '/performance/viewPerformanceModule') or normalize-space()='Performance']",
    )
    LOC_DIRECTORY_MENU = (
        By.XPATH,
        "//a[contains(@href, '/directory/viewDirectory') or normalize-space()='Directory']",
    )
    LOC_CLAIM_MENU = (
        By.XPATH,
        "//a[contains(@href, '/claim/viewClaimModule') or normalize-space()='Claim']",
    )
    LOC_BUZZ_MENU = (
        By.XPATH,
        "//a[contains(@href, '/buzz/viewBuzz') or normalize-space()='Buzz']",
    )
    LOC_DASHBOARD_MENU = (
        By.XPATH,
        "//a[contains(@href, '/dashboard/index') or normalize-space()='Dashboard']",
    )

    def is_state_on_dashboard(self) -> bool:
        return self.is_visible(*self.LOC_USER_DROPDOWN)

    def is_user_dropdown_visible(self) -> bool:
        return self.is_visible(*self.LOC_USER_DROPDOWN)

    def get_header_text(self) -> str:
        return wait_visible(self.driver, *self.LOC_HEADER, self.timeout).text.strip()

    def is_dashboard_header_visible(self) -> bool:
        return self.is_visible(*self.LOC_HEADER)

    # def get_visible_widgets_count(self) -> int:
    #     wait_url_contains(self.driver, "/dashboard", self.timeout)
    #     wait_visible(self.driver, *self.LOC_QUICK_LAUNCH, self.timeout)

    #     widgets = self.driver.find_elements(*self.LOC_WIDGETS)
    #     return len([widget for widget in widgets if widget.is_displayed()])
    
    # def get_visible_widget_title_count(self, widget_title: str) -> int:
    #     # Count widget containers that contain the given title and are visible.
    #     containers = self.driver.find_elements(*self.LOC_WIDGETS)
    #     count = 0
    #     for container in containers:
    #         try:
    #             title = container.find_element(By.XPATH, f".//*[normalize-space()='{widget_title}']")
    #             if container.is_displayed() and title.is_displayed():
    #                 count += 1
    #         except Exception:
    #             # title not found inside this container
    #             continue

    #     return count

    def action_logout(self) -> None:
        self.action_click(*self.LOC_USER_DROPDOWN)
        self.action_click(*self.LOC_LOGOUT)
        wait_url_contains(self.driver, "/auth/login", self.timeout)

    def action_refresh_dashboard(self) -> None:
        self.driver.refresh()
        wait_url_contains(self.driver, "/dashboard", self.timeout)
        wait_visible(self.driver, *self.LOC_HEADER, self.timeout)
        wait_visible(self.driver, *self.LOC_QUICK_LAUNCH, self.timeout)

    def is_time_at_work_visible(self) -> bool:
        return self.is_visible(*self.LOC_TIME_AT_WORK)

    def is_my_actions_visible(self) -> bool:
        return self.is_visible(*self.LOC_MY_ACTIONS)

    def is_quick_launch_visible(self) -> bool:
        return self.is_visible(*self.LOC_QUICK_LAUNCH)

    def is_employee_distribution_sub_unit_visible(self) -> bool:
        return self.is_visible(*self.LOC_EMPLOYEE_DISTRIBUTION_SUB_UNIT)

    def is_employee_distribution_location_visible(self) -> bool:
        return self.is_visible(*self.LOC_EMPLOYEE_DISTRIBUTION_LOCATION)

    def get_visible_quick_launch_shortcuts(self) -> list[str]:
        shortcuts = {
            "Assign Leave": self.LOC_ASSIGN_LEAVE,
            "Leave List": self.LOC_LEAVE_LIST,
            "Timesheets": self.LOC_TIMESHEETS,
            "Apply Leave": self.LOC_APPLY_LEAVE,
            "My Leave": self.LOC_MY_LEAVE,
            "My Timesheet": self.LOC_MY_TIMESHEET,
        }

        visible_shortcuts = []
        for shortcut_name, locator in shortcuts.items():
            if self.is_visible(*locator):
                visible_shortcuts.append(shortcut_name)

        return visible_shortcuts

    def action_click_sidebar_menu(self, by: By, locator: str) -> None:
        """Click a sidebar menu item. Use presence + JS click fallback to handle hidden/overlaid items."""
        self.action_ensure_sidebar_expanded()
        element = wait_present(self.driver, by, locator, self.timeout)
        try:
            if element.is_displayed():
                element.click()
            else:
                # element present but not visible - use JS click
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
                    element,
                )
        except Exception:
            # final fallback to JS click
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
                element,
            )

    def action_click_assign_leave(self) -> None:
        self.action_click(*self.LOC_ASSIGN_LEAVE)
        wait_url_contains(self.driver, "/leave/assignLeave", self.timeout)

    def action_click_leave_list(self) -> None:
        self.action_click(*self.LOC_LEAVE_LIST)
        wait_url_contains(self.driver, "/leave/viewLeaveList", self.timeout)

    def action_click_timesheets(self) -> None:
        self.action_click(*self.LOC_TIMESHEETS)
        wait_url_contains(self.driver, "/time/viewEmployeeTimesheet", self.timeout)

    def action_click_apply_leave(self) -> None:
        self.action_click(*self.LOC_APPLY_LEAVE)
        wait_url_contains(self.driver, "/leave/applyLeave", self.timeout)

    def action_click_my_leave(self) -> None:
        self.action_click(*self.LOC_MY_LEAVE)
        wait_url_contains(self.driver, "/leave/viewMyLeaveList", self.timeout)

    def action_click_my_timesheet(self) -> None:
        self.action_click(*self.LOC_MY_TIMESHEET)
        wait_url_contains(self.driver, "/time/viewMyTimesheet", self.timeout)

    def action_go_to_dashboard(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_DASHBOARD_MENU)
        wait_url_contains(self.driver, "/dashboard", self.timeout)

    def action_go_to_admin(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_ADMIN_MENU)
        wait_url_contains(self.driver, "/admin", self.timeout)

    def action_go_to_pim(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_PIM_MENU)
        wait_url_contains(self.driver, "/pim", self.timeout)

    def action_go_to_leave(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_LEAVE_MENU)
        wait_url_contains(self.driver, "/leave", self.timeout)

    def action_go_to_time(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_TIME_MENU)
        wait_url_contains(self.driver, "/time", self.timeout)

    def action_go_to_recruitment(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_RECRUITMENT_MENU)
        wait_url_contains(self.driver, "/recruitment", self.timeout)

    def action_go_to_my_info(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_MY_INFO_MENU)
        wait_url_contains(self.driver, "/pim/viewPersonalDetails", self.timeout)

    def action_go_to_performance(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_PERFORMANCE_MENU)
        wait_url_contains(self.driver, "/performance", self.timeout)

    def action_go_to_directory(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_DIRECTORY_MENU)
        wait_url_contains(self.driver, "/directory", self.timeout)

    def action_go_to_claim(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_CLAIM_MENU)
        wait_url_contains(self.driver, "/claim", self.timeout)

    def action_go_to_buzz(self) -> None:
        self.action_click_sidebar_menu(*self.LOC_BUZZ_MENU)
        wait_url_contains(self.driver, "/buzz", self.timeout)