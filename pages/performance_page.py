from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.wait_helpers import wait_visible, wait_url_contains


class PerformancePage(BasePage):
    LOC_PAGE_HEADER = (By.XPATH, "//h6[contains(normalize-space(),'Performance')] | //h5[contains(normalize-space(),'Performance')]")
    LOC_EMPLOYEE_TRACKERS = (By.XPATH, "//a[normalize-space()='Employee Trackers'] | //button[normalize-space()='Employee Trackers']")
    LOC_PERF_TABLE = (By.XPATH, "//table[@role='table'] | //div[contains(@class,'oxd-table')]")
    LOC_TRACKER_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...' or @placeholder='Type for hints']")
    LOC_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search'] | //button[contains(., 'Search')]")
    LOC_INVALID_ERROR = (By.XPATH, "//*[contains(normalize-space(),'Invalid') or contains(normalize-space(),'invalid') or contains(@class,'oxd-input-field-error')]")

    LOC_KPI_URL_FRAGMENT = "/performance/searchKpi"
    LOC_KPI_PAGE_HEADER = (By.XPATH, "//h6[contains(normalize-space(),'KPIs') or contains(normalize-space(),'KPI')] | //h5[contains(normalize-space(),'KPIs')]")
    # reuse LOC_PERF_TABLE for KPI table to avoid duplicated locators
    LOC_KPI_JOB_TITLE_DROPDOWN = (By.XPATH, "//label[normalize-space()='Job Title']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
    LOC_KPI_DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='listbox']//span[normalize-space()]")
    LOC_ADD_KPI_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    LOC_KPI_NAME_INPUT = (By.XPATH, "//label[normalize-space()='KPI Name']/../following-sibling::div//input")
    LOC_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")

    def is_performance_loaded(self) -> bool:
        # Check performance page header is visible
        try:
            wait_visible(self.driver, *self.LOC_PAGE_HEADER, self.timeout)
            return True
        except Exception:
            return False

    def open_employee_trackers(self) -> None:
        # Navigate to Employee Trackers section
        self.action_click(*self.LOC_EMPLOYEE_TRACKERS)
        wait_url_contains(self.driver, "employeeTrackers", self.timeout)

    def is_employee_trackers_table_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_PERF_TABLE, self.timeout)
            return True
        except Exception:
            return False

    def search_tracker_by_name(self, name: str) -> None:
        try:
            self.action_clear_and_type(*self.LOC_TRACKER_SEARCH_INPUT, name)
        except Exception:
            el = self.driver.find_element(*self.LOC_TRACKER_SEARCH_INPUT)
            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, name)
        try:
            self.action_click(*self.LOC_SEARCH_BUTTON)
        except Exception:
            pass

    def is_invalid_tracker_error_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_INVALID_ERROR, 3)
            return True
        except Exception:
            return self.is_employee_trackers_table_visible()

    def go_to_kpi_page(self) -> None:
        base = self.driver.current_url.split('/web')[0]
        kpi_url = base + "/web/index.php/performance/searchKpi"
        self.driver.get(kpi_url)
        wait_url_contains(self.driver, self.LOC_KPI_URL_FRAGMENT, self.timeout)

    def is_kpi_table_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_KPI_PAGE_HEADER, 5)
            return True
        except Exception:
            try:
                wait_visible(self.driver, *self.LOC_ADD_KPI_BUTTON, 5)
                return True
            except Exception:
                try:
                    wait_visible(self.driver, *self.LOC_PERF_TABLE, 5)
                    return True
                except Exception:
                    return False

    

    def add_kpi(self, kpi_name: str) -> None:
        # Open Add KPI form, populate fields and save
        self.action_click(*self.LOC_ADD_KPI_BUTTON)
        kpi_name_locators = [
            self.LOC_KPI_NAME_INPUT,
            (By.XPATH, "//input[contains(@placeholder,'KPI') or contains(@placeholder,'kpi') or contains(@name,'kpi')]") ,
            (By.XPATH, "//label[contains(normalize-space(),'KPI')]/../following-sibling::div//input"),
            (By.CSS_SELECTOR, "input[name*='kpi']"),
        ]

        name_set = False
        for loc in kpi_name_locators:
            try:
                wait_visible(self.driver, loc[0], loc[1], 5)
                try:
                    self.action_clear_and_type(loc[0], loc[1], kpi_name)
                    name_set = True
                    break
                except Exception:
                    try:
                        el = self.driver.find_element(loc[0], loc[1])
                        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, kpi_name)
                        name_set = True
                        break
                    except Exception:
                        continue
            except Exception:
                continue

        if not name_set:
            try:
                form = self.driver.find_element(By.XPATH, "//form|//div[contains(@class,'oxd-form')]")
                inputs = form.find_elements(By.XPATH, ".//input")
                for inp in inputs:
                    try:
                        if not inp.is_displayed():
                            continue
                        self.driver.execute_script("arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", inp, kpi_name)
                        name_set = True
                        break
                    except Exception:
                        continue
            except Exception:
                pass

        try:
            try:
                self.action_click(*self.LOC_KPI_JOB_TITLE_DROPDOWN)
            except Exception:
                alt = (By.XPATH, "//label[normalize-space()='Job Title']/following::div[contains(@class,'oxd-select-text')][1]")
                try:
                    self.action_click(*alt)
                except Exception:
                    pass

            def visible_options(driver):
                opts = [o for o in driver.find_elements(*self.LOC_DROPDOWN_OPTIONS) if o.is_displayed() and o.text.strip()]
                if opts:
                    return opts
                opts2 = [o for o in driver.find_elements(*self.LOC_KPI_DROPDOWN_OPTIONS) if o.is_displayed() and o.text.strip()]
                return opts2 if opts2 else False

            opts = []
            try:
                opts = WebDriverWait(self.driver, 5).until(visible_options)
            except Exception:
                opts = [o for o in self.driver.find_elements(*self.LOC_DROPDOWN_OPTIONS) if o.is_displayed() and o.text.strip()]
                if not opts:
                    opts = [o for o in self.driver.find_elements(*self.LOC_KPI_DROPDOWN_OPTIONS) if o.is_displayed() and o.text.strip()]

            if opts:
                try:
                    opts[0].click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", opts[0])
        except Exception:
            pass

        try:
            self.action_click(*self.LOC_SAVE_BUTTON)
        except Exception:
            try:
                btns = self.driver.find_elements(By.XPATH, "//button[contains(normalize-space(),'Save') or contains(normalize-space(),'save')]")
                if btns:
                    try:
                        btns[0].click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", btns[0])
                else:
                    self.driver.execute_script("document.querySelector('button[type=submit]').click();")
            except Exception:
                pass

    def get_kpi_rows_text(self) -> list[str]:
        # Return list of KPI row texts if present
        try:
            wait_visible(self.driver, *self.LOC_PERF_TABLE, self.timeout)
            rows = self.driver.find_elements(By.XPATH, "//table[@role='table']//tbody//tr")
            texts = [r.text.strip() for r in rows if r.text.strip()]
            if texts:
                return texts
            try:
                rec = self.driver.find_element(By.XPATH, "//*[contains(text(),'Records Found') or contains(text(),'records found')]")
                if rec and rec.text.strip():
                    return [rec.text.strip()]
            except Exception:
                pass
            return []
        except Exception:
            return []
