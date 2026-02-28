"""Элемент ссылки (link)"""
from .base_element import BaseElement
from playwright.sync_api import Locator
import allure
import logging

logger = logging.getLogger(__name__)


class LinkElement(BaseElement):
    """Ссылка"""

    def __init__(self, locator: Locator, name: str = None):
        super().__init__(locator, name or "ссылка")

    @allure.step("Получить URL ссылки '{name}'")
    def get_href(self) -> str:
        """Получение URL ссылки"""
        return self.get_attribute("href")