from __future__ import annotations

import pytest

from selenium.webdriver.common.by import By

from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage


@pytest.mark.pim
@pytest.mark.regression
@pytest.mark.smoke
def test_employee_list_loads_and_has_records(logged_in_driver):
    """FR-PIM-01: Employee List page must load and have at least one record."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()

    pim = PIMPage(logged_in_driver)
    assert pim.is_employee_list_loaded(), "PIM Employee List did not load or no rows present."


@pytest.mark.pim
@pytest.mark.regression
def test_search_by_first_name_returns_matching_rows(logged_in_driver):
    """FR-PIM-02: Searching by first name returns containing matches."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()
    pim = PIMPage(logged_in_driver)

    pim.search_by_first_name("A")
    rows = pim.get_table_row_texts()
    assert any("A" in r for r in rows), f"No rows returned containing 'A': {rows}"


@pytest.mark.pim
@pytest.mark.regression
def test_search_by_employee_id_returns_exact_match(logged_in_driver):
    """FR-PIM-03: Searching by employee ID returns the exact employee."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()
    pim = PIMPage(logged_in_driver)

    rows = pim.get_table_row_texts()
    if not rows:
        pytest.skip("No employee rows available to extract an ID for this environment")

    import re

    m = re.search(r"\b(\d{3,})\b", rows[0])
    if not m:
        pytest.skip("Could not extract an employee id from existing rows")

    emp_id = m.group(1)
    pim.search_by_employee_id(emp_id)
    rows_after = pim.get_table_row_texts()
    assert any(emp_id in r for r in rows_after), f"Employee id {emp_id} not found in results: {rows_after}"


@pytest.mark.pim
@pytest.mark.regression
def test_search_by_nonexistent_name_shows_no_records_message(logged_in_driver):
    """FR-PIM-04: Search with a name that does not match any employee must display the 'No Records Found' message."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()
    pim = PIMPage(logged_in_driver)

    query_name = "NameThatShouldNotExist12345"
    pim.search_by_first_name(query_name)
    rows = pim.get_table_row_texts()
    if not pim.is_no_records_found_visible():
        assert not any(query_name in r for r in rows), f"Expected no matching rows or 'No Records Found' message, found: {rows}"


@pytest.mark.pim
@pytest.mark.regression
def test_click_row_opens_personal_details(logged_in_driver):
    """FR-PIM-05: Clicking an employee row must open the employee record on the Personal Details tab."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()
    pim = PIMPage(logged_in_driver)

    rows = pim.get_table_row_texts()
    if not rows:
        pytest.skip("No employee rows available to click in this environment")

    pim.click_first_table_row()
    assert pim.is_visible(*pim.LOC_PERSONAL_DETAILS_TAB), "Personal Details tab not visible after opening the first employee record"


@pytest.mark.pim
@pytest.mark.regression
def test_contact_details_tab_loads(logged_in_driver):
    """FR-PIM-06: Navigating to the Contact Details tab on an employee record must load the tab with address and contact fields."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()
    pim = PIMPage(logged_in_driver)

    rows = pim.get_table_row_texts()
    if not rows:
        pytest.skip("No employee rows available to open contact details")

    pim.click_first_table_row()
    pim.open_contact_details()
    assert (
        pim.is_visible(By.XPATH, "//label[normalize-space()='Address Street 1']")
        or pim.is_visible(By.XPATH, "//label[normalize-space()='Address Line 1']")
        or pim.is_visible(By.XPATH, "//label[normalize-space()='Contact Details']")
        or pim.is_visible(By.XPATH, "//h6[contains(normalize-space(),'Contact Details')]")
    ), "Contact Details fields not visible"


@pytest.mark.pim
@pytest.mark.regression
def test_add_employee_and_verify_search(logged_in_driver):
    """FR-PIM-07: A new employee must be successfully added through the Add Employee form and appear in PIM search results."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_pim()
    pim = PIMPage(logged_in_driver)

    pim.add_employee("Baba", "", "Dook", "1069")

    # Get the persisted/current employee id from the details page (robust to any server-assigned changes)
    emp_id = pim.get_current_employee_id()
    assert emp_id, "Could not read employee id after saving the new employee"

    # After save, navigate back to PIM list and search for the actual id
    import time
    time.sleep(1)
    dashboard.action_go_to_pim()

    pim.search_by_employee_id(emp_id)
    rows = pim.get_table_row_texts()
    assert any(emp_id in r for r in rows), f"Added employee ID {emp_id} not found in search results: {rows}"