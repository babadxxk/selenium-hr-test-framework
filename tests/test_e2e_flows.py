from __future__ import annotations

import pytest

from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.time_page import TimePage
from pages.admin_page import AdminPage
from pages.recruitment_page import RecruitmentPage
from utils.wait_helpers import wait_visible


@pytest.mark.e2e
def test_e2e_pim_flow(driver, auth_credentials):
    """FR-E2E-01: Login -> PIM table loads -> Dashboard -> Logout."""
    username, password = auth_credentials

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    pim = PIMPage(driver)

    login.action_login(username=username, password=password)
    assert dashboard.is_state_on_dashboard(), "Login failed or dashboard not visible"

    dashboard.action_go_to_pim()
    assert pim.is_employee_list_loaded(), "PIM records table did not load"

    dashboard.action_go_to_dashboard()
    assert dashboard.is_dashboard_header_visible(), "Dashboard did not load after returning"

    dashboard.action_logout()
    assert login.is_state_on_login_page(), "Logout did not return to login page"


@pytest.mark.e2e
def test_e2e_time_flow(driver, auth_credentials):
    """FR-E2E-02: Login -> Time timesheet loads -> Dashboard -> Logout."""
    username, password = auth_credentials

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    time_page = TimePage(driver)

    login.action_login(username=username, password=password)
    assert dashboard.is_state_on_dashboard(), "Login failed or dashboard not visible"

    dashboard.action_go_to_time()
    assert time_page.is_employee_timesheets_loaded(), "Timesheet records did not load"

    dashboard.action_go_to_dashboard()
    assert dashboard.is_dashboard_header_visible(), "Dashboard did not load after returning"

    dashboard.action_logout()
    assert login.is_state_on_login_page(), "Logout did not return to login page"


@pytest.mark.e2e
def test_e2e_admin_job_flow(driver, auth_credentials):
    """FR-E2E-03: Login -> Admin > System Users -> verify user table -> Dashboard -> Logout."""
    username, password = auth_credentials

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    admin = AdminPage(driver)

    login.action_login(username=username, password=password)
    assert dashboard.is_state_on_dashboard(), "Login failed or dashboard not visible"

    dashboard.action_go_to_admin()
    assert admin.is_system_users_loaded(), "System Users page did not load"
    rows = admin.get_table_row_texts()
    assert rows or admin.is_no_records_found_visible(), "User record table not present"
    # return to dashboard then logout
    dashboard.action_go_to_dashboard()
    assert dashboard.is_dashboard_header_visible(), "Dashboard did not load after returning"

    dashboard.action_logout()
    assert login.is_state_on_login_page(), "Logout did not return to login page"


@pytest.mark.e2e
def test_e2e_recruitment_flow(driver, auth_credentials):
    """FR-E2E-04: Login -> Recruitment Vacancies -> Candidates -> Logout."""
    username, password = auth_credentials

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    recruitment = RecruitmentPage(driver)

    login.action_login(username=username, password=password)
    assert dashboard.is_state_on_dashboard(), "Login failed or dashboard not visible"

    dashboard.action_go_to_recruitment()
    # Vacancies may appear as a header or table; click sidebar item and check for vacancy header
    dashboard.action_click_sidebar_item("Vacancies")
    wait_visible(driver, By.XPATH, "//h6[normalize-space()='Vacancies'] | //h5[normalize-space()='Vacancies'] | //*[normalize-space()='Vacancies']", 10)

    # Now go to Candidates and verify candidate list
    dashboard.action_click_sidebar_item("Candidates")
    assert recruitment.is_candidates_page_loaded(), "Candidates page did not load or candidate list unavailable"

    dashboard.action_logout()
    assert login.is_state_on_login_page(), "Logout did not return to login page"
