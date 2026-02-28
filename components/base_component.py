"""Базовый класс для всех компонентов"""
from playwright.sync_api import Page, Locator
import logging

logger = logging.getLogger(__name__)


class BaseComponent:
    """Базовый компонент с root-локатором"""

    def __init__(self, page: Page, root_locator: Locator = None, name: str = None):
        self.page = page
        self.name = name or "компонент"
        self.root = root_locator or page
        self.logger = logging.getLogger(self.__class__.__name__)

    def _locator(self, selector: str) -> Locator:
        """Получение локатора относительно root компонента"""
        return self.root.locator(selector)

    @property
    def selector(self) -> str:
        """Property: получение селектора корневого элемента"""
        try:
            return str(self.root._selector) if hasattr(self.root, '_selector') else "page"
        except:
            return ""