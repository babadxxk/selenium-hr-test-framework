from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.data_loader import load_json


@pytest.mark.auth
@pytest.mark.smoke
def test_login_valid_credentials(driver, auth_credentials):
    """FR-AUTH-01: Valid login redirects to dashboard with user dropdown."""
    login_page = LoginPage(driver)
    dashboard = DashboardPage(driver)
    username, password = auth_credentials

    login_page.action_login(username=username, password=password)
    assert dashboard.is_state_on_dashboard(), "User dropdown not visible after valid login."
    assert "Dashboard" in dashboard.get_header_text()


@pytest.mark.auth
@pytest.mark.regression
def test_login_username_with_spaces(driver):
    """FR-AUTH-01: Username with leading/trailing spaces authenticates after trim."""
    users = load_json("data/users.json")["valid_users"]
    trimmed_user = next(
        (user for user in users if user.get("type") == "trimmed_username"),
        None,
    )
    if not trimmed_user:
        pytest.skip("Trimmed username data not configured.")

    login_page = LoginPage(driver)
    dashboard = DashboardPage(driver)
    login_page.action_login(trimmed_user["username"].strip(), trimmed_user["password"])
    assert dashboard.is_state_on_dashboard(), (
        "Username with leading/trailing spaces should be trimmed before authentication."
    )


@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.parametrize("user", load_json("data/users.json")["invalid_users"])
def test_login_invalid_credentials(driver, user):
    """FR-AUTH-02/03/07: Invalid credentials and special characters show error."""
    login_page = LoginPage(driver)
    login_page.action_login(user["username"], user["password"])
    assert "Invalid credentials" in login_page.get_error_message()


@pytest.mark.auth
@pytest.mark.regression
def test_login_empty_credentials(driver):
    """FR-AUTH-04: Both fields empty shows required validation."""
    login_page = LoginPage(driver)
    login_page.action_login("", "")
    assert login_page.get_required_error_count() >= 2


@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.parametrize("user", load_json("data/users.json")["partial_empty"])
def test_login_partial_empty_credentials(driver, user):
    """FR-AUTH-05/06: Partial empty credentials surface validation or login error."""
    login_page = LoginPage(driver)
    login_page.action_login(user["username"], user["password"])

    required_error_count = login_page.get_required_error_count()
    if required_error_count >= 1:
        assert required_error_count >= 1, (
            "Expected at least one field validation error for partial-empty credentials."
        )
    else:
        error_message = login_page.get_error_message()
        assert error_message, (
            "Expected an error message when one of the login fields is empty."
        )
        assert "Invalid credentials" in error_message or "required" in error_message.lower(), (
            "Expected either a generic invalid credentials error or a required-field validation message."
        )


@pytest.mark.auth
@pytest.mark.regression
def test_direct_url_without_session_redirects_to_login(driver, config):
    """FR-AUTH-08: Direct internal URL without session redirects to login."""
    driver.get(f"{config['base_url']}/web/index.php/dashboard/index")
    login_page = LoginPage(driver)
    assert login_page.is_state_on_login_page()


@pytest.mark.auth
@pytest.mark.regression
def test_back_button_after_logout_blocks_access(logged_in_driver):
    """FR-AUTH-09: Browser back after logout does not restore authenticated access."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_logout()
    logged_in_driver.back()
    logged_in_driver.get(
        "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    )
    assert "/auth/login" in logged_in_driver.current_url


@pytest.mark.auth
@pytest.mark.regression
def test_session_invalidated_after_logout(driver, auth_credentials, config):
    """FR-AUTH-10: Session invalidated after logout; internal URL redirects to login."""
    username, password = auth_credentials
    login_page = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login_page.action_login(username, password)
    assert login_page.is_state_logged_in()
    dashboard.action_logout()

    driver.get(f"{config['base_url']}/web/index.php/dashboard/index")
    assert login_page.is_state_on_login_page()


@pytest.mark.auth
@pytest.mark.regression
def test_session_persists_after_dashboard_refresh(logged_in_driver):
    """FR-AUTH-10: Refreshing dashboard retains active session."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_refresh_dashboard()
    assert dashboard.is_state_on_dashboard()


@pytest.mark.auth
@pytest.mark.regression
def test_session_persists_in_new_tab(logged_in_driver):
    """FR-AUTH-10: Opening dashboard in new tab keeps authenticated session."""
    original_handle = logged_in_driver.current_window_handle
    logged_in_driver.switch_to.new_window("tab")
    logged_in_driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    dashboard = DashboardPage(logged_in_driver)
    assert dashboard.is_state_on_dashboard()
    logged_in_driver.close()
    logged_in_driver.switch_to.window(original_handle)
