from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.buzz_page import BuzzPage


@pytest.mark.buzz
def test_buzz_feed_loads_with_existing_post(logged_in_driver):
    """FR-BUZZ-01: Buzz feed page must load and display the post feed with at least one existing post."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_buzz()

    page = BuzzPage(logged_in_driver)
    assert page.is_buzz_loaded(), "Buzz feed did not load or no feed element found ('.orangehrm-buzz')"


@pytest.mark.buzz
def test_buzz_post_input_placeholder_visible(logged_in_driver):
    """FR-BUZZ-02: The 'What's on your mind?' text input area must be visible at the top of the Buzz Newsfeed."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_buzz()

    page = BuzzPage(logged_in_driver)
    placeholder = page.get_post_input_placeholder()
    assert placeholder and "What's on your mind" in placeholder, "Post input placeholder not found or does not contain expected text"


@pytest.mark.buzz
def test_buzz_photo_video_button_visible(logged_in_driver):
    """FR-BUZZ-03: The photo/video share button must be visible alongside the text post area."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_buzz()

    page = BuzzPage(logged_in_driver)
    assert page.is_photo_video_button_visible(), "Photo/Video share button not visible on Buzz feed"


@pytest.mark.buzz
def test_buzz_create_post_and_appears_on_top(logged_in_driver):
    """FR-BUZZ-04: Creating a post should show the new post at top of Most Recent posts."""
    dashboard = DashboardPage(logged_in_driver)
    dashboard.action_go_to_buzz()

    page = BuzzPage(logged_in_driver)
    text = f"Automated post {__import__('uuid').uuid4().hex[:6]}"
    page.create_post(text)

    latest = page.get_latest_post_text()
    assert latest and text in latest, "Newly created post not found at top of feed"
