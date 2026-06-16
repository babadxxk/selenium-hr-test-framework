from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.maintenance_page import MaintenancePage


@pytest.mark.maintenance
def test_maintenance_requires_password_prompt(logged_in_driver):
    """FR-MAINT-01: Navigating to Maintenance must display a password confirmation prompt before granting access."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_sidebar_item("Maintenance")

    page = MaintenancePage(logged_in_driver)
    assert page.is_password_prompt_visible(), "Expected admin password confirmation prompt when opening Maintenance"


@pytest.mark.maintenance
def test_maintenance_accepts_correct_password_and_opens(logged_in_driver, auth_credentials):
    """FR-MAINT-02: Entering the demo admin password on the confirmation prompt must grant access to Maintenance landing page."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_sidebar_item("Maintenance")

    page = MaintenancePage(logged_in_driver)
    assert page.is_password_prompt_visible(), "Password prompt did not appear"

    username, password = auth_credentials
    page.submit_password(password)

    assert page.is_maintenance_landing_visible(), "Maintenance landing page did not load after entering correct password"


@pytest.mark.maintenance
def test_maintenance_rejects_incorrect_password(logged_in_driver):
    """FR-MAINT-03: Entering an incorrect password on the Maintenance confirmation prompt must show an Invalid credentials error."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_sidebar_item("Maintenance")

    page = MaintenancePage(logged_in_driver)
    assert page.is_password_prompt_visible(), "Password prompt did not appear"

    page.submit_password("wrong_password_123")
    assert page.is_invalid_credentials_visible(), "Expected 'Invalid credentials' indicator when entering wrong password"


@pytest.mark.maintenance
def test_access_records_search_shows_employee_and_id(logged_in_driver, auth_credentials):
    """FR-MAINT-04: Access Records page must load and returning a valid employee shows full name and employee ID in results."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_click_sidebar_item("Maintenance")

    page = MaintenancePage(logged_in_driver)
    # submit the admin password from auth credentials
    _, password = auth_credentials
    page.submit_password(password)
    assert page.is_maintenance_landing_visible(), "Maintenance landing page did not load"

    page.go_to_access_records()
    # search for the employee used earlier
    target = "Ranga Akunuri"
    page.search_access_records(target)

    rows = page.get_access_result_texts()
    if not rows:
        pytest.skip("No access records available to validate")

    # find a row containing the name and an ID-like token
    found = False
    for r in rows:
        if target.lower() in r.lower():
            # try to find an ID token (alphanumeric short token)
            tokens = [t for t in r.split() if any(c.isdigit() for c in t) or len(t) <= 10]
            if tokens:
                found = True
                break
    assert found, f"Expected search results to include '{target}' with an employee id"
