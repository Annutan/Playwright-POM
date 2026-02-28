"""Элемент ввода"""
import allure
from playwright.sync_api import Locator, TimeoutError as PlaywrightTimeoutError
from .base_element import BaseElement
import logging

logger = logging.getLogger(__name__)


class InputElement(BaseElement):
    """Элемент ввода (input, textarea)"""

    def __init__(self, locator: Locator, name: str = None):
        super().__init__(locator, name or "поле ввода")

    def fill(self, text: str) -> 'InputElement':
        """Заполнение поля ввода"""
        with allure.step(f"Заполнить {self.name}: '{text}'"):
            logger.info(f"Заполняю {self.name}: '{text}'")
            try:
                # Сначала ждем видимости элемента
                self.wait_for_visible(timeout=10000)
                self.locator.fill(text)
            except PlaywrightTimeoutError:
                logger.error(f"Не удалось найти элемент {self.name} для заполнения")
                raise
        return self

    def clear(self) -> 'InputElement':
        """Очистка поля ввода"""
        with allure.step(f"Очистить {self.name}"):
            logger.info(f"Очищаю {self.name}")
            try:
                # Сначала ждем видимости элемента
                self.wait_for_visible(timeout=10000)

                # Несколько способов очистки для надежности
                self.locator.clear()

                # Дополнительная проверка, что поле действительно очистилось
                current_value = self.get_value()
                if current_value:
                    logger.warning(f"Поле {self.name} не очистилось полностью. Текущее значение: '{current_value}'")
                    # Пробуем очистить через выделение и удаление
                    self.locator.press("Control+a")
                    self.locator.press("Delete")
            except PlaywrightTimeoutError:
                logger.error(f"Не удалось найти элемент {self.name} для очистки")
                raise
        return self

    def get_value(self) -> str:
        """Получение значения поля ввода"""
        try:
            # Ждем видимости перед получением значения
            self.wait_for_visible(timeout=5000)
            value = self.locator.input_value()
            logger.debug(f"Значение {self.name}: '{value}'")
            return value
        except:
            return ""

    def clear_and_fill(self, text: str) -> 'InputElement':
        """Очистить и заполнить поле ввода"""
        # Сначала проверяем видимость
        self.wait_for_visible(timeout=10000)

        # Очищаем
        self.clear()

        # Проверяем что очистилось
        current_value = self.get_value()
        if current_value:
            logger.warning(f"Поле не очистилось, пробую принудительную очистку")
            self.locator.evaluate("el => el.value = ''")

        # Заполняем
        self.fill(text)

        # Проверяем что заполнилось
        filled_value = self.get_value()
        if filled_value != text:
            logger.warning(f"Значение не совпадает. Ожидалось: '{text}', получено: '{filled_value}'")
            # Пробуем заполнить через evaluate
            self.locator.evaluate(f"el => el.value = '{text}'")

        return self

    def press_enter(self) -> 'InputElement':
        """Нажать Enter в поле ввода"""
        with allure.step(f"Нажать Enter в {self.name}"):
            logger.info(f"Нажимаю Enter в {self.name}")
            self.wait_for_visible()
            self.locator.press("Enter")
        return self

    def press_tab(self) -> 'InputElement':
        """Нажать Tab в поле ввода"""
        with allure.step(f"Нажать Tab в {self.name}"):
            self.wait_for_visible()
            self.locator.press("Tab")
        return self