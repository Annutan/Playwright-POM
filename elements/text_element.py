"""
Текстовый элемент (span, div, p, etc.)
Базовый элемент для работы с текстом
"""
from playwright.sync_api import Locator
from .base_element import BaseElement
import logging

logger = logging.getLogger(__name__)


class TextElement(BaseElement):
    """
    Базовый текстовый элемент.
    Используется для элементов, которые в основном отображают текст.
    """
    def __init__(self, locator: Locator, name: str = None):
        super().__init__(locator, name or "текстовый элемент")

    def contains_text(self, text: str) -> bool:
        """Проверка наличия текста в элементе"""
        element_text = self.get_text()
        return text in element_text

    def get_text_lines(self) -> list:
        """Получение текста по строкам"""
        text = self.get_text()
        return [line.strip() for line in text.split('\n') if line.strip()]