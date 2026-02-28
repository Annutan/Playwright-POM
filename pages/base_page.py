"""Базовый класс для всех страниц"""
import allure
from playwright.sync_api import Page
from ..elements.base_element import BaseElement
from ..elements.input_element import InputElement
from ..elements.button_element import ButtonElement
from ..elements.link_element import LinkElement
from ..elements.text_element import TextElement
from ..elements.modal_element import ModalElement
from ..elements.table_element import TableElement
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    # ===== ФАБРИЧНЫЕ МЕТОДЫ ДЛЯ СОЗДАНИЯ ЭЛЕМЕНТОВ =====
    # (используются редко, обычно элементы создаются в __init__)

    def create_element(self, selector: str, name: str = None) -> BaseElement:
        """Создание базового элемента по селектору"""
        locator = self.page.locator(selector)
        return BaseElement(locator, name)

    def create_input(self, selector: str, name: str = None) -> InputElement:
        """Создание элемента ввода"""
        locator = self.page.locator(selector)
        return InputElement(locator, name)

    def create_button(self, selector: str, name: str = None) -> ButtonElement:
        """Создание кнопки"""
        locator = self.page.locator(selector)
        return ButtonElement(locator, name)

    def create_link(self, selector: str, name: str = None) -> LinkElement:
        """Создание ссылки"""
        locator = self.page.locator(selector)
        return LinkElement(locator, name)

    def create_text(self, selector: str, name: str = None) -> TextElement:
        """Создание текстового элемента"""
        locator = self.page.locator(selector)
        return TextElement(locator, name)

    def create_modal(self, selector: str, name: str = None) -> ModalElement:
        """Создание модального окна"""
        locator = self.page.locator(selector)
        return ModalElement(locator, name)

    def create_table(self, selector: str, name: str = None) -> TableElement:
        """Создание таблицы"""
        locator = self.page.locator(selector)
        return TableElement(locator, name)

    # ===== ОБЩИЕ МЕТОДЫ =====

    def navigate(self, url: str) -> 'BasePage':
        """Переход по URL с проверкой дублирования /app"""
        with allure.step(f"Переход по URL: {url}"):
            # Если URL уже содержит /app, а мы пытаемся добавить еще один
            if "/app" in self.page.url and "/app" in url:
                # Используем URL как есть
                self.page.goto(url)
            else:
                self.page.goto(url)

            self.logger.info(f"Перешли на {self.page.url}")
        return self

    def wait(self, milliseconds: int) -> 'BasePage':
        """Ожидание"""
        self.page.wait_for_timeout(milliseconds)
        return self

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Скриншот страницы"""
        return self.page.screenshot()

    def get_page_title(self) -> str:
        """Получение заголовка страницы"""
        return self.page.title()

    def get_current_url(self) -> str:
        """Получение текущего URL"""
        return self.page.url

    def refresh(self) -> 'BasePage':
        """Обновить страницу"""
        self.page.reload()
        return self