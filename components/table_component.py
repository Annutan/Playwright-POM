"""
Компонент таблицы со строками
Использует table_element как базовый и добавляет логику работы со строками
"""
import allure
from playwright.sync_api import Page, Locator
from .base_component import BaseComponent
from ..elements.table_element import TableElement
from ..elements.button_element import ButtonElement
from ..elements.link_element import LinkElement
from ..elements.text_element import TextElement
from ..locators.audiences_locators import AudienceRowLocators, AudiencesPageLocators
import logging

logger = logging.getLogger(__name__)


class TableRowComponent(BaseComponent):
    """Компонент строки таблицы"""

    def __init__(self, page: Page, root_locator: Locator, name: str = "строка таблицы"):
        super().__init__(page, root_locator, name)

    @property
    def cells(self):
        """Генератор ячеек строки"""
        cells = self._locator("td, [role='cell']")
        count = cells.count()

        for i in range(count):
            cell_locator = cells.nth(i)
            yield TextElement(cell_locator, name=f"{self.name} - ячейка {i}")

    @allure.step("Получить текст ячейки {index} в строке")
    def get_cell_text(self, index: int) -> str:
        """Получение текста ячейки по индексу"""
        cells = self._locator("td, [role='cell']")
        if index < cells.count():
            cell = TextElement(cells.nth(index), f"{self.name} - ячейка {index}")
            return cell.get_text()
        return ""

    @allure.step("Получить кнопку действия '{action}' в строке")
    def get_action_button(self, action: str) -> ButtonElement:
        """Получение кнопки действия"""
        button = self._locator(f"button:has-text('{action}')").first
        return ButtonElement(button, name=f"{self.name} - кнопка '{action}'")

    @allure.step("Получить ссылку в строке")
    def get_link(self) -> LinkElement:
        """Получение первой ссылки в строке"""
        link = self._locator("a").first
        return LinkElement(link, name=f"{self.name} - ссылка")

    @allure.step("Кликнуть по строке")
    def click(self):
        """Клик по строке"""
        self.root.click()
        return self

    @allure.step("Проверить что строка содержит текст '{text}'")
    def contains_text(self, text: str) -> bool:
        """Проверка наличия текста в строке"""
        row_text = self.root.text_content() or ""
        return text.lower() in row_text.lower()

    @property
    def is_visible(self) -> bool:
        """Проверка видимости строки"""
        try:
            return self.root.is_visible(timeout=1000)
        except:
            return False


class TableComponent(BaseComponent):
    """Компонент таблицы с поддержкой строк"""

    def __init__(self, page: Page, root_locator: Locator, name: str = "таблица"):
        super().__init__(page, root_locator, name)

        # Создаем базовый элемент таблицы
        self.table = TableElement(
            root_locator,
            name=f"{self.name} - базовый элемент"
        )

    @property
    def rows(self):
        """Генератор строк таблицы"""
        rows = self._locator(AudiencesPageLocators.TABLE_ROWS)
        count = rows.count()

        for i in range(count):
            row_locator = rows.nth(i)
            yield TableRowComponent(self.page, row_locator, name=f"{self.name} - строка {i}")

    # Убираем дублирование - просто делегируем к table
    @property
    def row_count(self) -> int:
        """Количество строк"""
        try:
            rows = self._locator(AudiencesPageLocators.TABLE_ROWS)
            count = rows.count()
            logger.info(f"Количество строк в таблице: {count}")
            return count
        except Exception as e:
            logger.error(f"Ошибка при подсчете строк: {e}")
            return 0

    @property
    def is_empty(self) -> bool:
        """Проверка пустой таблицы"""
        return self.table.is_empty

    def wait_for_data(self, timeout: int = 5000) -> 'TableComponent':
        """Ожидание данных в таблице"""
        self.table.wait_for_data(timeout)
        return self

    # УНИКАЛЬНЫЙ метод компонента (преобразует Locator в TableRowComponent)
    @allure.step("Получить строку по индексу {index}")
    def get_row_by_index(self, index: int = 0) -> TableRowComponent:
        """Получение строки по индексу"""
        row_locator = self.table.get_row(index)
        return TableRowComponent(
            self.page,
            row_locator,
            name=f"{self.name} - строка {index}"
        )

    # УНИКАЛЬНЫЙ метод компонента
    @allure.step("Найти строку по имени аудитории '{audience_name}'")
    def find_row_by_audience_name(self, audience_name: str) -> TableRowComponent:
        """Поиск строки по имени аудитории"""
        row_locator = self.page.locator(AudienceRowLocators.row_by_name(audience_name))
        row_locator.wait_for(state="visible", timeout=10000)

        return TableRowComponent(
            self.page,
            row_locator,
            name=f"{self.name} - строка аудитории '{audience_name}'"
        )

    # УНИКАЛЬНЫЙ метод компонента
    @allure.step("Получить все названия аудиторий в таблице")
    def get_all_audience_names(self) -> list:
        """Получение всех названий аудиторий"""
        names = []
        try:
            name_links = self._locator("a")

            for i in range(name_links.count()):
                link = name_links.nth(i)
                name = link.text_content().strip()
                if name and name not in names:
                    names.append(name)
        except Exception as e:
            logger.error(f"Ошибка при получении названий аудиторий: {e}")

        return names

