from __future__ import annotations

import uuid

import pytest

from pages.dashboard_page import DashboardPage
from pages.performance_page import PerformancePage


@pytest.mark.performance
@pytest.mark.regression
def test_performance_employee_trackers_shows_table(logged_in_driver):
    """FR-PERF-01: Employee Trackers page must load with a records table when opened from Performance."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_performance()

    perf = PerformancePage(logged_in_driver)
    assert perf.is_performance_loaded(), "Performance page did not load"

    try:
        perf.open_employee_trackers()
    except Exception:
        pass

    assert perf.is_employee_trackers_table_visible(), "Employee Trackers table not visible"


@pytest.mark.performance
def test_performance_employee_tracker_search_shows_invalid_error(logged_in_driver):
    """FR-PERF-02: Searching Employee Trackers with an invalid/non-existent employee name must display an invalid-field validation error."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_performance()
    perf = PerformancePage(logged_in_driver)

    try:
        perf.open_employee_trackers()
    except Exception:
        pass

    perf.search_tracker_by_name("Admin")
    assert perf.is_invalid_tracker_error_visible(), "Expected invalid-field error when searching with Admin"


@pytest.mark.performance
def test_kpi_page_loads_and_has_table(logged_in_driver):
    """FR-PERF-03: KPIs configuration page must load and display the KPI list table."""
    perf = PerformancePage(logged_in_driver)
    perf.go_to_kpi_page()
    assert perf.is_kpi_table_visible(), "KPI table not visible on KPI page"


@pytest.mark.performance
def test_add_kpi_creates_new_kpi_record(logged_in_driver):
    """FR-PERF-04: Adding a KPI with valid KPI Name and Job Title must create a new KPI record visible in the KPI list."""
    perf = PerformancePage(logged_in_driver)
    perf.go_to_kpi_page()
    assert perf.is_kpi_table_visible(), "KPI table not visible"

    name = f"AutoKPI_{uuid.uuid4().hex[:6]}"
    perf.add_kpi(name)

    # Page-level helper handles refresh + polling and returns whether KPI is visible
    assert perf.verify_kpi_present(name, timeout=10), f"New KPI '{name}' not found in KPI list"
