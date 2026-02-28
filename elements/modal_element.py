"""
Элемент модального окна (modal)
Базовый элемент, только общие методы для модальных окон
"""
from playwright.sync_api import Locator
from .base_element import BaseElement
import logging

logger = logging.getLogger(__name__)


class ModalElement(BaseElement):
    """
    Базовый элемент модального окна.
    Содержит только методы для работы с модальным окном как с целым.
    Конкретные кнопки (Да/Отмена) должны находиться в компоненте.
    """
    def __init__(self, locator: Locator, name: str = "модальное окно"):
        super().__init__(locator, name)

    @property
    def is_open(self) -> bool:
        """Проверка, открыто ли модальное окно"""
        return self.is_visible(timeout=1000)

    @property
    def is_closed(self) -> bool:
        """Проверка, закрыто ли модальное окно"""
        return not self.is_open

    def get_body_text(self) -> str:
        """Получение текста модального окна"""
        return self.get_text()

    def wait_for_open(self, timeout: int = 5000) -> 'ModalElement':
        """Ожидание открытия модального окна"""
        return self.wait_for_visible(timeout)

    def wait_for_close(self, timeout: int = 5000) -> 'ModalElement':
        """Ожидание закрытия модального окна"""
        return self.wait_for_hidden(timeout)