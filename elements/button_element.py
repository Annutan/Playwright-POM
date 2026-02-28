"""Кнопка"""
import allure
from playwright.sync_api import Locator
from .base_element import BaseElement
import logging

logger = logging.getLogger(__name__)


class ButtonElement(BaseElement):
    """Кнопка (button)"""

    def __init__(self, locator: Locator, name: str = None):
        # ТОЛЬКО Locator!
        super().__init__(locator, name or "кнопка")

    def click_and_wait(self, timeout: int = 5000) -> 'ButtonElement':
        """Кликнуть и подождать"""
        self.click()
        import time
        time.sleep(timeout / 1000)
        return self