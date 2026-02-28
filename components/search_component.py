"""
Компонент поиска
"""
import allure
from playwright.sync_api import Page
from ..elements.input_element import InputElement
from .base_component import BaseComponent
import logging

logger = logging.getLogger(__name__)


class SearchComponent(BaseComponent):
    """Компонент поиска"""

    def __init__(self, page: Page, selector: str, name: str = "компонент поиска"):
        """
        Инициализация компонента поиска
        :param page: экземпляр страницы
        :param selector: селектор поля ввода (XPath или CSS)
        :param name: имя компонента
        """
        self.page = page
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)
        self._selector = selector

        # Поле ввода поиска - создаем InputElement напрямую
        self.search_input = InputElement(
            page.locator(selector),
            name=f"{self.name} - поле ввода"
        )

    @allure.step("Выполнить поиск: '{search_text}'")
    def search(self, search_text: str) -> 'SearchComponent':
        """Выполнить поиск (рабочая версия как в начале)"""
        logger.info(f"Выполняю поиск: '{search_text}'")

        # Ожидаем видимости поля
        self.search_input.wait_for_visible(timeout=5000)

        # Очищаем поле и вводим текст
        self.search_input.clear()
        self.search_input.fill(search_text)

        # Нажимаем Enter для применения фильтрации
        self.search_input.press_enter()

        # Небольшая пауза для обновления таблицы
        self.page.wait_for_timeout(500)

        return self

    @allure.step("Очистить поиск")
    def clear_search(self) -> 'SearchComponent':
        """Очистить поле поиска"""
        logger.info("Очищаю поле поиска")

        self.search_input.wait_for_visible(timeout=5000)
        self.search_input.clear()
        self.page.wait_for_timeout(500)

        return self

    @allure.step("Получить текущее значение поиска")
    def get_value(self) -> str:
        """Получить текущее значение поля поиска"""
        return self.search_input.get_value()

    @allure.step("Проверить что поиск пуст")
    def is_empty(self) -> bool:
        """Проверка, что поле поиска пустое"""
        return self.get_value() == ""