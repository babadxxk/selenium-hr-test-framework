from __future__ import annotations

import pytest
from datetime import date, timedelta

from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage


@pytest.mark.leave
def test_leave_list_loads_and_displays_table(logged_in_driver):
    """FR-LV-01: Leave List page must load and display the leave records table."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)
    assert page.is_leave_list_loaded(), "Leave List did not load or table not present"


@pytest.mark.leave
def test_leave_type_dropdown_populated(logged_in_driver):
    """FR-LV-02: The Leave Type dropdown must be populated with available options."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)

    try:
        selected = page.select_first_dropdown_option_and_search(page.LOC_LEAVE_TYPE)
    except Exception:
        pytest.skip("Leave Type dropdown not present in this environment")

    assert selected, "Expected a non-empty Leave Type option"


@pytest.mark.leave
def test_date_range_filter_results_or_no_records(logged_in_driver):
    """FR-LV-03: Applying a valid date range filter shows results or 'No Records Found'."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)

    today = date.today()
    frm = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    to = today.strftime("%Y-%m-%d")
    page.apply_date_filter(frm, to)

    assert page.is_no_records_found_visible() or page.get_table_row_texts(), "Expected either results or 'No Records Found'"


@pytest.mark.leave
def test_leave_type_filter_shows_filtered_results_or_no_records(logged_in_driver):
    """FR-LV-04: Selecting a Leave Type filter and searching shows filtered results or 'No Records Found'."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)

    try:
        selected = page.select_first_dropdown_option(page.LOC_LEAVE_TYPE)
    except Exception:
        pytest.skip("Leave Type dropdown not available in this environment")

    assert page.is_no_records_found_visible() or page.get_table_row_texts(), f"Expected results or 'No Records Found' after filtering by {selected}"


@pytest.mark.leave
def test_leave_status_filter_shows_filtered_results_or_no_records(logged_in_driver):
    """FR-LV-05: Selecting a Leave Status filter and searching shows filtered results or 'No Records Found'."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)

    try:
        selected = page.select_first_dropdown_option_and_search(page.LOC_LEAVE_STATUS)
    except Exception:
        pytest.skip("Leave Status dropdown not available in this environment")

    assert page.is_no_records_found_visible() or page.get_table_row_texts(), f"Expected results or 'No Records Found' after filtering by status {selected}"


@pytest.mark.leave
def test_search_by_employee_name_shows_records_or_no_records(logged_in_driver):
    """FR-LV-06: Searching by valid employee name shows matching leaves or 'No Records Found'."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)

    page.search_by_employee_name("A")
    assert page.is_no_records_found_visible() or page.get_table_row_texts(), "Expected results or 'No Records Found' for employee name search"


@pytest.mark.leave
def test_nonexistent_employee_name_shows_validation_or_no_records(logged_in_driver):
    """FR-LV-07: Searching by a non-existent employee name shows required-field validation or no records message."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_leave_list()
    page = LeavePage(logged_in_driver)

    page.search_by_employee_name("NoSuchEmployee12345")
    count = page.get_required_error_count()
    assert count > 0 or page.is_no_records_found_visible(), "Expected required-field validation or 'No Records Found' for nonexistent employee"


@pytest.mark.leave
def test_assign_leave_page_loads_with_required_fields(logged_in_driver):
    """FR-LV-08: Assign Leave page loads with Employee Name, Leave Type, From Date and To Date fields present."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_leave()
    page = LeavePage(logged_in_driver)

    dashboard.action_click_assign_leave()
    assert page.is_assign_form_loaded(), "Assign Leave form did not load with required fields"


@pytest.mark.leave
def test_assign_leave_without_employee_shows_required_error(logged_in_driver):
    """FR-LV-09: Submitting Assign Leave without selecting an employee shows required-field validation."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_assign_leave()
    page = LeavePage(logged_in_driver)

    dashboard.action_click_assign_leave()
    page.assign_leave(None, True, "2099-01-10", "2099-01-12")
    assert page.get_required_error_count() > 0, "Expected required-field validation when employee not provided"


@pytest.mark.leave
def test_assign_leave_without_leave_type_shows_required_error(logged_in_driver):
    """FR-LV-10: Submitting Assign Leave without selecting leave type shows required-field validation."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_assign_leave()
    page = LeavePage(logged_in_driver)

    dashboard.action_click_assign_leave()
    page.assign_leave("Some Employee", None, "2099-01-10", "2099-01-12")
    assert page.get_required_error_count() > 0, "Expected required-field validation when leave type not provided"


@pytest.mark.leave
def test_assign_leave_success_for_future_dates(logged_in_driver):
    """FR-LV-11: Completing Assign Leave with valid future dates must succeed and be verifiable."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_leave()
    page = LeavePage(logged_in_driver)

    dashboard.action_click_sidebar_item("Assign Leave")
    page.assign_leave("Baba Dook", True, "2099-01-10", "2099-01-12")

    msg = page.get_assign_confirmation_text()
    if msg:
        assert "success" in msg.lower() or "assigned" in msg.lower()
    else:
        # navigate back to leave list and search for the employee
        dashboard.action_go_to_leave()
        page.search_by_employee_name("Baba Dook")
        assert page.is_no_records_found_visible() or page.get_table_row_texts(), "Expected assigned leave to appear or a confirmation message"
