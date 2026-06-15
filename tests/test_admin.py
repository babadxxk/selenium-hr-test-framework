from __future__ import annotations

import pytest

from pages.admin_page import AdminPage
from pages.dashboard_page import DashboardPage


@pytest.mark.admin
@pytest.mark.regression
def test_system_users_page_loads_and_shows_user_list(logged_in_driver):
    """FR-ADM-01: System Users page must load and display the user list table."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    # Verify the Admin dashboard redirects to System Users and shows the user table
    assert admin.is_system_users_loaded(), "System Users page did not load successfully."
    rows = admin.get_table_row_texts()
    assert rows, "Expected user list rows on System Users page."


@pytest.mark.admin
@pytest.mark.regression
def test_searching_by_username_returns_matching_rows(logged_in_driver):
    """FR-ADM-02: Searching by a username must return matching user rows."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    # Search for the known Admin username and confirm matching rows appear
    admin.search_username("Admin")

    rows = admin.get_table_row_texts()
    assert rows, "Expected at least one matching row for username 'Admin'."
    assert any("Admin" in row for row in rows), f"Expected rows containing 'Admin', got {rows}"


@pytest.mark.admin
@pytest.mark.regression
def test_filter_by_user_role_returns_only_admin_rows(logged_in_driver):
    """FR-ADM-03: Filtering by User Role dropdown must return only users with that role."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    # Filter the system users by Admin role and verify all returned rows contain Admin
    admin.filter_user_role("Admin")

    rows = admin.get_table_row_texts()
    assert rows, "Expected rows after filtering by User Role 'Admin'."
    assert all("Admin" in row for row in rows), f"Expected only Admin role rows, got {rows}"


@pytest.mark.admin
@pytest.mark.regression
def test_filter_by_status_returns_only_enabled_rows(logged_in_driver):
    """FR-ADM-04: Filtering by Status must return users matching that status."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    # Filter the system users by Enabled status and verify all rows are enabled
    admin.filter_status("Enabled")

    rows = admin.get_table_row_texts()
    assert rows, "Expected rows after filtering by Status 'Enabled'."
    assert all("Enabled" in row for row in rows), f"Expected only Enabled rows, got {rows}"


@pytest.mark.admin
@pytest.mark.regression
def test_add_user_form_loads_with_required_fields(logged_in_driver):
    """FR-ADM-05: Add User form must load when the Add button is clicked; User Role, Employee Name, Status, Username and Password fields must be present."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    # Open the Add User form and confirm required form fields are visible
    admin.open_add_user_form()

    assert admin.is_add_user_form_loaded(), "Add User form did not show all required fields."


@pytest.mark.admin
@pytest.mark.regression
def test_add_user_form_requires_username(logged_in_driver):
    """FR-ADM-06: Submitting Add User form with Username empty must show required-field validation."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    admin.open_add_user_form()
    # Leave username empty and submit to verify required validation appears
    admin.submit_add_user_form(
        user_role="Admin",
        employee_name="Admin",
        status="Enabled",
        username="",
        password="Password123!",
        confirm_password="Password123!",
    )

    messages = admin.get_add_user_validation_messages()
    assert messages, f"Expected required-field validation messages, got {messages}"


@pytest.mark.admin
@pytest.mark.regression
def test_add_user_form_password_mismatch_shows_error(logged_in_driver):
    """FR-ADM-07: Submitting Add User form with Password and Confirm Password mismatched must show a password mismatch error."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_admin()

    admin = AdminPage(logged_in_driver)
    admin.open_add_user_form()
    # Submit with mismatched passwords and verify a password mismatch error is displayed
    admin.submit_add_user_form(
        user_role="Admin",
        employee_name="Admin",
        status="Enabled",
        username="newuser123",
        password="Password123!",
        confirm_password="Password1234!",
    )

    messages = admin.get_add_user_validation_messages()
    assert any("match" in msg.lower() or "password" in msg.lower() for msg in messages), (
        f"Expected password mismatch validation message, got {messages}"
    )

