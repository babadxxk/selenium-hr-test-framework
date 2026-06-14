from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.dashboard
@pytest.mark.smoke
def test_dashboard_header_visible_after_login(logged_in_driver):
    """FR-DASH-01: After login, Dashboard heading must be visible."""
    dashboard_page = DashboardPage(logged_in_driver)

    assert dashboard_page.get_header_text() == "Dashboard"


@pytest.mark.dashboard
@pytest.mark.smoke
def test_dashboard_main_widgets_visible(logged_in_driver):
    """FR-DASH-02, FR-DASH-03: Time at Work and My Actions widgets must be visible."""
    dashboard_page = DashboardPage(logged_in_driver)

    assert dashboard_page.is_time_at_work_visible(), (
        "Time at Work widget is not visible."
    )
    assert dashboard_page.is_my_actions_visible(), (
        "My Actions widget is not visible."
    )


@pytest.mark.dashboard
@pytest.mark.smoke
def test_quick_launch_panel_and_shortcuts_visible(logged_in_driver):
    """FR-DASH-04: Quick Launch panel must contain all required shortcuts."""
    dashboard_page = DashboardPage(logged_in_driver)

    assert dashboard_page.is_quick_launch_visible(), (
        "Quick Launch panel is not visible."
    )

    expected_shortcuts = [
        "Assign Leave",
        "Leave List",
        "Timesheets",
        "Apply Leave",
        "My Leave",
        "My Timesheet",
    ]

    actual_shortcuts = dashboard_page.get_visible_quick_launch_shortcuts()

    for shortcut in expected_shortcuts:
        assert shortcut in actual_shortcuts, (
            f"Expected shortcut '{shortcut}' not found. "
            f"Actual shortcuts: {actual_shortcuts}"
        )


@pytest.mark.dashboard
@pytest.mark.regression
def test_dashboard_chart_widgets_visible(logged_in_driver):
    """FR-DASH-05, FR-DASH-06: Employee distribution chart widgets must render without error."""
    dashboard_page = DashboardPage(logged_in_driver)

    assert dashboard_page.is_employee_distribution_sub_unit_visible(), (
        "Employee Distribution by Sub Unit widget is not visible."
    )
    assert dashboard_page.is_employee_distribution_location_visible(), (
        "Employee Distribution by Location widget is not visible."
    )


@pytest.mark.dashboard
@pytest.mark.regression
@pytest.mark.parametrize(
    "action_name, expected_url",
    [
        ("action_click_assign_leave", "/leave/assignLeave"),
        ("action_click_leave_list", "/leave/viewLeaveList"),
        ("action_click_timesheets", "/time/viewEmployeeTimesheet"),
        ("action_click_apply_leave", "/leave/applyLeave"),
        ("action_click_my_leave", "/leave/viewMyLeaveList"),
        ("action_click_my_timesheet", "/time/viewMyTimesheet"),
    ],
)
def test_quick_launch_navigation(logged_in_driver, action_name, expected_url):
    """
    FR-DASH-07:
    Each Quick Launch shortcut must navigate to the correct page.
    """
    dashboard_page = DashboardPage(logged_in_driver)

    assert dashboard_page.is_state_on_dashboard(), (
        "Dashboard must be loaded before quick-launch navigation tests run."
    )

    action = getattr(dashboard_page, action_name)
    action()

    assert expected_url.lower() in logged_in_driver.current_url.lower(), (
        f"Expected URL to contain '{expected_url}', "
        f"but actual URL was '{logged_in_driver.current_url}'."
    )


@pytest.mark.dashboard
@pytest.mark.regression
@pytest.mark.parametrize(
    "action_name, expected_url",
    [
        ("action_go_to_admin", "/admin"),
        ("action_go_to_pim", "/pim"),
        ("action_go_to_leave", "/leave"),
        ("action_go_to_time", "/time"),
        ("action_go_to_recruitment", "/recruitment"),
        ("action_go_to_my_info", "/pim/viewPersonalDetails"),
        ("action_go_to_performance", "/performance"),
        ("action_go_to_directory", "/directory"),
        ("action_go_to_claim", "/claim"),
        ("action_go_to_buzz", "/buzz"),
    ],
)
def test_dashboard_side_menu_navigation(logged_in_driver, action_name, expected_url):
    """
    FR-DASH-08:
    Side navigation items from Dashboard must navigate correctly.
    """
    dashboard_page = DashboardPage(logged_in_driver)

    assert dashboard_page.is_state_on_dashboard(), (
        "Dashboard must be loaded before side menu navigation tests run."
    )

    action = getattr(dashboard_page, action_name)
    action()

    assert expected_url.lower() in logged_in_driver.current_url.lower(), (
        f"Expected URL to contain '{expected_url}', "
        f"but actual URL was '{logged_in_driver.current_url}'."
    )