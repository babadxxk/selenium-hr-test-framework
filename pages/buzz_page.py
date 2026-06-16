from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.wait_helpers import wait_visible


class BuzzPage(BasePage):
    LOC_BUZZ_FEED = (By.CSS_SELECTOR, ".orangehrm-buzz")
    LOC_POST_INPUT = (
        By.XPATH,
        "//textarea[@placeholder=\"What's on your mind?\"] | //input[@placeholder=\"What's on your mind?\"] | //div[contains(@class,'oxd-editor')]//textarea",
    )
    LOC_PHOTO_VIDEO_BUTTON = (By.XPATH, "//button[contains(., 'Photo') or contains(., 'Photo/Video') or contains(@aria-label,'photo')]")
    LOC_POST_BUTTON = (By.XPATH, "//button[normalize-space()='Post'] | //button[contains(., 'Post')]")
    LOC_POSTS_LIST = (By.XPATH, "//div[contains(@class,'oxd-buzz-list')] | //div[contains(@class,'orangehrm-buzz')]//div[contains(@class,'post') or contains(@class,'oxd-card')]")
    LOC_MOST_RECENT_TAB = (By.XPATH, "//*[contains(normalize-space(),'Most Recent Posts') or contains(normalize-space(),'Most Recent')]")

    def is_buzz_loaded(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_BUZZ_FEED, self.timeout)
            return True
        except Exception:
            return False

    def get_post_input_placeholder(self) -> str | None:
        try:
            el = wait_visible(self.driver, *self.LOC_POST_INPUT, self.timeout)
            return el.get_attribute("placeholder") or el.text or None
        except Exception:
            return None

    def is_photo_video_button_visible(self) -> bool:
        try:
            wait_visible(self.driver, *self.LOC_PHOTO_VIDEO_BUTTON, self.timeout)
            return True
        except Exception:
            return False

    def create_post(self, text: str) -> None:
        try:
            input_el = wait_visible(self.driver, *self.LOC_POST_INPUT, self.timeout)
            try:
                input_el.clear()
            except Exception:
                pass
            try:
                input_el.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", input_el)
                    input_el.click()
                except Exception:
                    pass

            tag = input_el.tag_name.lower()
            is_contenteditable = str(input_el.get_attribute('contenteditable')).lower() == 'true'
            if tag == 'div' or is_contenteditable:
                try:
                    js = (
                        "arguments[0].innerText = arguments[1];"
                        "arguments[0].textContent = arguments[1];"
                        "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                        "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));"
                        "arguments[0].dispatchEvent(new KeyboardEvent('keyup',{key:'a'}));"
                    )
                    self.driver.execute_script(js, input_el, text)
                except Exception:
                    try:
                        input_el.send_keys(text)
                    except Exception:
                        pass
            else:
                try:
                    input_el.clear()
                except Exception:
                    pass
                try:
                    input_el.send_keys(text)
                except Exception:
                    try:
                        self.driver.execute_script(
                            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
                            input_el,
                            text,
                        )
                    except Exception:
                        pass
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_POST_INPUT)
                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", el, text)
            except Exception:
                pass
        try:
            before_count = len(self.driver.find_elements(*self.LOC_POSTS_LIST))
        except Exception:
            before_count = None

        try:
            self.action_click(*self.LOC_POST_BUTTON)
        except Exception:
            try:
                el = self.driver.find_element(*self.LOC_POST_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                pass

        self._last_post_text = text

        try:
            if before_count is not None:
                WebDriverWait(self.driver, 20).until(
                    lambda d: len(d.find_elements(*self.LOC_POSTS_LIST)) > before_count
                )
            else:
                found = self.wait_for_post_text(text, timeout=20)
                if not found:
                    try:
                        self.action_click(*self.LOC_MOST_RECENT_TAB)
                    except Exception:
                        pass
                    self.wait_for_post_text(text, timeout=10)
        except Exception:
            try:
                self.wait_for_post_text(text, timeout=10)
            except Exception:
                pass

    def find_post_card_by_text(self, text: str, timeout: int = 10):
        """Return the post/card element that contains the given text, or None."""
        try:
            xpath_text = f"//*[contains(normalize-space(),'{text}')]"
            WebDriverWait(self.driver, timeout).until(lambda d: d.find_elements(By.XPATH, xpath_text))
            xpath_card = f"{xpath_text}/ancestor::div[contains(@class,'post') or contains(@class,'oxd-card')][1]"
            el = self.driver.find_element(By.XPATH, xpath_card)
            return el
        except Exception:
            return None

    def get_latest_post_text(self) -> str | None:
        try:
            last = getattr(self, "_last_post_text", None)
            if last:
                try:
                    found = self.wait_for_post_text(last, timeout=15)
                    if found:
                        xpath_text = f"//*[contains(normalize-space(),'{last}')]"
                        elems = self.driver.find_elements(By.XPATH, xpath_text)
                        for e in elems:
                            try:
                                t = e.text.strip()
                            except Exception:
                                continue
                            if t and last in t:
                                return t
                except Exception:
                    pass

            xpath_cards = (
                "//div[contains(@class,'orangehrm-buzz') or contains(@class,'oxd-buzz-list')]"
                "//div[(contains(@class,'post') or contains(@class,'oxd-card'))]"
            )
            try:
                xpath_first_real = (
                    "(" + xpath_cards + 
                    "[not(.//textarea) and not(.//input) and not(.//button[contains(normalize-space(),'Post')]) and not(.//button[contains(normalize-space(),'Share')])])[1]"
                )
                el = self.driver.find_element(By.XPATH, xpath_first_real)
                txt = el.text.strip()
                if txt and not any(k in txt for k in ("Share Photos", "Share Video", "What's on your mind", "Post", "Share")):
                    return txt
            except Exception:
                pass

            try:
                cards = self.driver.find_elements(By.XPATH, xpath_cards)
                for p in cards:
                    try:
                        txt = p.text.strip()
                    except Exception:
                        continue
                    if not txt:
                        continue
                    if any(k in txt for k in ("Share Photos", "Share Video", "What's on your mind", "Post", "Share")):
                        continue
                    return txt
            except Exception:
                pass

            return None
        except Exception:
            return None

    def wait_for_post_text(self, text: str, timeout: int = 15) -> bool:
        """Wait until an element containing the given post text appears."""
        try:
            xpath = f"//*[contains(normalize-space(),'{text}')]"
            WebDriverWait(self.driver, timeout).until(lambda d: d.find_elements(By.XPATH, xpath))
            return True
        except Exception:
            return False
