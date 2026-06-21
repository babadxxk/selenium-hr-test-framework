from __future__ import annotations

import uuid

import pytest
from selenium.webdriver.common.by import By

from pages.dashboard_page import DashboardPage
from pages.claim_page import ClaimPage


@pytest.mark.claim
def test_submit_claim_page_loads_with_fields(logged_in_driver):
    """FR-CLAIM-01: Employee Claims page must load and display the records table."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_claim()

    page = ClaimPage(logged_in_driver)
    page.go_to_employee_claims()
    assert page.is_records_table_visible(), "Employee Claims records table not visible"


@pytest.mark.claim
def test_event_dropdown_populated(logged_in_driver):
    """FR-CLAIM-02: The Event dropdown on Submit Claim must be populated with at least one claim event."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_claim()

    page = ClaimPage(logged_in_driver)
    page.go_to_submit_claim()
    opts = page.get_event_options()
    assert opts, "Expected at least one Event option in dropdown"


@pytest.mark.claim
def test_submit_claim_without_event_shows_required_error(logged_in_driver):
    """FR-CLAIM-03: Submitting the Submit Claim form without selecting an Event must show a required-field validation error."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_claim()

    page = ClaimPage(logged_in_driver)
    page.go_to_submit_claim()

    page.submit_claim_without_event()
    assert page.is_required_error_visible() or page.get_required_error_count() > 0, "Expected required-field validation when submitting without Event"


@pytest.mark.claim
def test_add_event_creates_new_event_record(logged_in_driver):
    """FR-CLAIM-04: Add Event flow must require Event Name and create new event visible in list after save."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_claim()

    page = ClaimPage(logged_in_driver)
    page.go_to_events_config()
    if not page.is_events_list_visible():
        pytest.skip("Claim Events configuration not available in this environment")

    page.add_event(None)
    assert page.get_required_error_count() > 0, "Expected required-field validation when saving without Event Name"

    name = f"AutoEvent_{uuid.uuid4().hex[:6]}"
    page.add_event(name)
    import time

    found = False
    end = time.time() + 45
    while time.time() < end:
        try:
            if page.event_exists(name):
                found = True
                break
        except Exception:
            pass
        try:
            logged_in_driver.refresh()
        except Exception:
            pass
        time.sleep(1)

    assert found, f"New event '{name}' not found in events list after retrying"
