"""
Элемент таблицы (table)
Базовый элемент для работы с таблицами
"""
from playwright.sync_api import Locator
from .base_element import BaseElement
import logging

logger = logging.getLogger(__name__)


class TableElement(BaseElement):
    """
    Базовый элемент таблицы.
    Содержит методы для работы с таблицей как с целым.
    Поиск конкретных строк должен быть в компоненте.
    """
    def __init__(self, locator: Locator, name: str = "таблица"):
        super().__init__(locator, name)

    @property
    def row_count(self) -> int:
        """Количество строк в таблице"""
        try:
            # Используем property для получения селектора строк
            # Селектор строк должен быть определен в компоненте, не здесь!
            # Этот метод просто считает дочерние элементы
            return self.locator.count()
        except Exception as e:
            logger.error(f"Ошибка при подсчете строк: {e}")
            return 0

    @property
    def is_empty(self) -> bool:
        """Проверка, пустая ли таблица"""
        return self.row_count == 0

    def get_row(self, index: int) -> Locator:
        """
        Получение строки по индексу.
        Возвращает Locator, а не BaseElement,
        потому что конкретный тип строки определит компонент
        """
        return self.locator.nth(index)

    def wait_for_data(self, timeout: int = 5000) -> 'TableElement':
        """Ожидание появления данных в таблице"""
        # Ждем, пока появится хотя бы одна строка
        self.locator.first.wait_for(state="attached", timeout=timeout)
        return self