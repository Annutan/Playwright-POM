"""Базовый класс для всех элементов"""
import allure
from playwright.sync_api import Locator, TimeoutError as PlaywrightTimeoutError
import logging

logger = logging.getLogger(__name__)


class BaseElement:
    """Базовый элемент с общими методами"""

    def __init__(self, locator: Locator, name: str = None):
        self.locator = locator
        self.name = name or "элемент"

    @property
    def selector(self) -> str:
        """Получение селектора элемента (property)"""
        try:
            selector = str(self.locator)
            if "Locator@" in selector:
                selector = selector.replace("Locator@", "")
            logger.debug(f"Селектор {self.name}: '{selector}'")
            return selector
        except:
            return ""

    def click(self) -> 'BaseElement':
        """Клик по элементу"""
        with allure.step(f"Кликнуть на {self.name}"):
            logger.debug(f"Кликаю на {self.name}")
            try:
                self.wait_for_visible(timeout=10000)
                self.locator.click()
            except PlaywrightTimeoutError:
                logger.error(f"Не удалось кликнуть на {self.name} - элемент не найден")
                raise
        return self

    def is_visible(self, timeout: int = 5000) -> bool:
        """Проверка видимости элемента"""
        try:
            return self.locator.is_visible(timeout=timeout)
        except:
            return False

    def is_enabled(self) -> bool:
        """Проверка доступности элемента"""
        try:
            return self.locator.is_enabled()
        except:
            return False

    def wait_for_visible(self, timeout: int = 10000) -> 'BaseElement':
        """Ожидание видимости элемента"""
        with allure.step(f"Ожидание видимости {self.name}"):
            logger.debug(f"Жду видимости {self.name}")
            try:
                self.locator.wait_for(state="visible", timeout=timeout)
            except PlaywrightTimeoutError:
                logger.error(f"Элемент {self.name} не стал видимым за {timeout}мс")

                # Пробуем найти элемент на странице для отладки
                try:
                    count = self.locator.count()
                    logger.error(f"Количество найденных элементов с таким локатором: {count}")
                except:
                    pass

                raise
        return self

    def wait_for_hidden(self, timeout: int = 10000) -> 'BaseElement':
        """Ожидание скрытия элемента"""
        with allure.step(f"Ожидание скрытия {self.name}"):
            logger.debug(f"Жду скрытия {self.name}")
            self.locator.wait_for(state="hidden", timeout=timeout)
        return self

    def get_text(self) -> str:
        """Получение текста элемента"""
        try:
            self.wait_for_visible(timeout=5000)
            text = self.locator.text_content() or ""
            logger.debug(f"Текст {self.name}: '{text}'")
            return text.strip()
        except:
            return ""

    def get_attribute(self, name: str) -> str:
        """Получение атрибута элемента"""
        try:
            self.wait_for_visible(timeout=5000)
            attr = self.locator.get_attribute(name) or ""
            logger.debug(f"Атрибут {name} {self.name}: '{attr}'")
            return attr
        except:
            return ""

    def count(self) -> int:
        """Получение количества элементов"""
        return self.locator.count()
