from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path
from typing import Generator

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pages.login_page import LoginPage
from utils.driver_factory import create_chrome_driver
from utils.logger import get_logger


LOGGER = get_logger(__name__)


@pytest.fixture(scope="session")
def config() -> dict:
    with (PROJECT_ROOT / "config" / "config.yml").open(encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="function")
def driver(config: dict) -> Generator:
    webdriver = create_chrome_driver(headless=config.get("headless", True))
    webdriver.explicit_wait = config.get("timeouts", {}).get("explicit_wait_seconds", 15)
    webdriver.get(config["base_url"])
    yield webdriver
    webdriver.quit()


@pytest.fixture(scope="function")
def auth_credentials(config: dict) -> tuple[str, str]:
    username = os.getenv(config["credentials"]["username_env"], "Admin")
    password = os.getenv(config["credentials"]["password_env"], "admin123")
    return username, password


@pytest.fixture(scope="function")
def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]


@pytest.fixture(scope="function")
def logged_in_driver(driver, auth_credentials):
    username, password = auth_credentials
    login_page = LoginPage(driver)
    login_page.action_login(username=username, password=password)
    assert login_page.is_state_logged_in(), "Precondition failed: login unsuccessful."
    login_page.action_dismiss_blocking_overlays()
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    web_driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
    if not web_driver:
        return

    screenshots_dir = PROJECT_ROOT / "reports" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    screenshot_file = screenshots_dir / f"{item.name}.png"
    web_driver.save_screenshot(str(screenshot_file))
    LOGGER.info("Saved failure screenshot: %s", screenshot_file.as_posix())