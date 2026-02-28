"""Page Object для страницы аудиторий на Playwright"""
import allure
from playwright.sync_api import Page
from .base_page import BasePage
from ..components.table_component import TableComponent
from ..components.search_component import SearchComponent
from ..components.form_component import FormComponent
from ..components.modal_component import ModalComponent
from ..elements.button_element import ButtonElement
from ..elements.base_element import BaseElement
from ..locators.audiences_locators import (
    AudiencesPageLocators,
    AudienceFormLocators,
    ModalLocators,
    AudienceRowLocators
)
import logging

logger = logging.getLogger(__name__)


class AudiencesPage(BasePage):
    """Страница аудиторий на Playwright"""

    def __init__(self, page: Page):
        super().__init__(page)

        # Основные элементы страницы
        self.add_button = ButtonElement(
            self.page.locator(AudiencesPageLocators.ADD_BUTTON),
            name="кнопка 'Добавить аудиторию'"
        )

        # Компоненты (ленивая инициализация)
        self._table = None
        self._search = None
        self._form = None
        self._modal = None

    @allure.step("Ожидать загрузки страницы аудиторий")
    def wait_for_page_load(self, timeout: int = 20000) -> 'AudiencesPage':
        """Ожидание загрузки страницы аудиторий"""
        self.logger.info("Ожидаю загрузку страницы аудиторий")

        # Ждем появления кнопки "Добавить аудиторию"
        try:
            self.add_button.wait_for_visible(timeout)
            self.logger.info("Страница аудиторий загружена")
        except Exception as e:
            self.logger.error(f"Страница аудиторий не загрузилась: {e}")

            # Делаем скриншот для отладки
            allure.attach(
                self.page.screenshot(),
                name="page_load_timeout",
                attachment_type=allure.attachment_type.PNG
            )

            # Сохраняем текущий URL
            allure.attach(
                f"Current URL: {self.page.url}",
                name="current_url",
                attachment_type=allure.attachment_type.TEXT
            )

            raise

        return self

    @property
    def table(self) -> TableComponent:
        """Компонент таблицы аудиторий"""
        if self._table is None:
            self._table = TableComponent(
                self.page,
                root_locator=self.page.locator(AudiencesPageLocators.TABLE_CONTAINER),
                name="таблица аудиторий"
            )
        return self._table

    @property
    def search(self) -> SearchComponent:
        """Компонент поиска"""
        if self._search is None:
            # Используем упрощенный конструктор
            from test_frontend_settings.components.search_component import SearchComponent
            self._search = SearchComponent(
                self.page,
                selector=AudiencesPageLocators.SEARCH_INPUT,
                name="поиск аудиторий"
            )
        return self._search

    @allure.step("Отладка: проверить поле поиска")
    def debug_search_field(self) -> dict:
        """Отладочный метод для проверки поля поиска"""
        debug_info = {}

        try:
            # Проверяем видимость поля
            search_field = self.page.locator(AudiencesPageLocators.SEARCH_INPUT)
            debug_info['is_visible'] = search_field.is_visible(timeout=3000)
            debug_info['selector'] = AudiencesPageLocators.SEARCH_INPUT

            if debug_info['is_visible']:
                # Получаем атрибуты
                debug_info['placeholder'] = search_field.get_attribute('placeholder')
                debug_info['tag_name'] = search_field.evaluate("el => el.tagName")
                debug_info['type'] = search_field.get_attribute('type')

                # Пробуем ввести текст
                search_field.click()
                search_field.fill("test")
                debug_info['filled_value'] = search_field.input_value()

                # Очищаем
                search_field.clear()
                debug_info['cleared_value'] = search_field.input_value()

        except Exception as e:
            debug_info['error'] = str(e)

        # Прикрепляем скриншот
        allure.attach(
            self.page.screenshot(),
            name="debug_search_field_screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        return debug_info

    @property
    def form(self) -> FormComponent:
        """Компонент формы аудитории"""
        if self._form is None:
            self._form = FormComponent(
                self.page,
                form_locators=AudienceFormLocators,
                name="форма аудитории"
            )
        return self._form

    @property
    def modal(self) -> ModalComponent:
        """Компонент модального окна"""
        if self._modal is None:
            # Получаем локатор модального окна из locators
            modal_locator = self.page.locator(ModalLocators.MODAL_DIALOG)

            self._modal = ModalComponent(
                self.page,
                root_locator=modal_locator,
                name="модальное окно подтверждения"
            )
        return self._modal

    # ===== МЕТОДЫ ДЛЯ РАБОТЫ С АУДИТОРИЯМИ =====

    @allure.step("Проверить наличие аудитории '{name}'")
    def is_audience_present(self, name: str, timeout: int = 2000) -> bool:
        """Проверка наличия аудитории через готовые локаторы"""
        try:
            row_locator = AudienceRowLocators.row_by_name(name)
            row_element = BaseElement(
                self.page.locator(row_locator),
                name=f"строка аудитории '{name}'"
            )

            # Пробуем найти сразу
            if row_element.is_visible(timeout=timeout):
                logger.info(f"Аудитория '{name}' найдена")
                return True

            # Если не нашли, ждем немного и пробуем еще раз
            self.page.wait_for_timeout(500)
            is_visible = row_element.is_visible(timeout=timeout)
            if is_visible:
                logger.info(f"Аудитория '{name}' найдена после повторной проверки")

            return is_visible

        except Exception as e:
            logger.debug(f"Ошибка при проверке наличия аудитории '{name}': {e}")
            return False

    @allure.step("Открыть аудиторию '{name}' для редактирования")
    def open_audience_for_edit(self, name: str) -> 'AudiencesPage':
        """Открытие аудитории через локатор ссылки"""
        name_link_locator = AudienceRowLocators.name_link_by_name(name)
        name_link = BaseElement(
            self.page.locator(name_link_locator),
            name=f"ссылка на аудиторию '{name}'"
        )
        name_link.click()
        return self

    @allure.step("Инициировать удаление аудитории '{name}'")
    def initiate_delete_audience(self, name: str) -> 'AudiencesPage':
        """Инициирование удаления через локатор кнопки"""
        delete_btn_locator = AudienceRowLocators.delete_button_by_name(name)
        delete_btn = ButtonElement(
            self.page.locator(delete_btn_locator),
            name=f"кнопка удаления аудитории '{name}'"
        )
        delete_btn.click()
        return self

    @allure.step("Получить статус аудитории '{name}'")
    def get_audience_status(self, name: str) -> bool:
        """Получение статуса аудитории через локатор"""
        status_locator = AudienceRowLocators.status_by_name(name)
        status_element = BaseElement(
            self.page.locator(status_locator),
            name=f"статус аудитории '{name}'"
        )

        if status_element.is_visible():
            aria_checked = status_element.get_attribute("aria-checked")
            return aria_checked == "true"
        return False

    @allure.step("Проверить наличие индикатора '{indicator}' у аудитории '{audience_name}'")
    def audience_has_indicator(self, audience_name: str, indicator: str) -> bool:
        """Проверка наличия индикатора в строке таблицы"""
        try:
            row = self.table.find_row_by_audience_name(audience_name)
            return row.contains_text(indicator)
        except Exception as e:
            logger.debug(f"Ошибка при проверке индикатора: {e}")
            return False


    # ===== ВЫСОКОУРОВНЕВЫЕ МЕТОДЫ =====

    @allure.step("Создать аудиторию: '{name}' с индикатором '{indicator}'")
    def create_audience(self, name: str, indicator: str = None) -> 'AudiencesPage':
        """Создание аудитории через компоненты"""
        self.logger.info(f"Создаю аудиторию: '{name}'")

        self.add_button.click()
        self.form.fill_name(name)

        if indicator:
            self.form.add_positive_indicator(indicator)

        self.form.save()
        self.table.wait_for_data()
        return self

    @allure.step("Удалить аудиторию '{name}'")
    def delete_audience(self, name: str, confirm: bool = True) -> 'AudiencesPage':
        """Удаление аудитории через компоненты"""
        self.logger.info(f"Удаляю аудиторию: '{name}'")

        # Инициируем удаление
        self.initiate_delete_audience(name)

        # Ждем появления модального окна
        self.modal.wait_for_open(timeout=5000)

        # Подтверждаем или отменяем
        if confirm:
            self.modal.confirm()
        else:
            self.modal.cancel()

        # Ждем закрытия модального окна
        self.modal.wait_for_close(timeout=5000)

        # Ждем обновления таблицы
        self.page.wait_for_timeout(2000)

        return self

    @allure.step("Проверить что поиск работает корректно")
    def verify_search_works(self, search_text: str) -> bool:
        """
        Проверка, что поиск действительно фильтрует таблицу
        Возвращает True, если поиск работает
        """
        # Сохраняем текущее количество записей
        initial_count = self.table.row_count
        logger.info(f"Начальное количество записей: {initial_count}")

        # Выполняем поиск
        self.search.search(search_text)
        self.page.wait_for_timeout(1000)

        # Проверяем, что количество изменилось
        new_count = self.table.row_count
        logger.info(f"Количество записей после поиска '{search_text}': {new_count}")

        # Очищаем поиск
        self.search.clear_search()

        return new_count < initial_count or new_count == 1

    @allure.step("Выполнить поиск аудитории '{search_text}'")
    def search_audience(self, search_text: str) -> 'AudiencesPage':
        """Поиск аудитории"""
        self.search.search(search_text)
        return self

    @allure.step("Очистить поиск")
    def clear_search(self) -> 'AudiencesPage':
        """Очистка поиска"""
        self.search.clear_search()
        return self


    # === МЕТОДЫ ДЛЯ РАБОТЫ С ИНДИКАТОРАМИ (ПРОКСИ МЕТОДЫ К КОМПОНЕНТУ ФОРМЫ) ===

    @allure.step("Добавить позитивный индикатор: '{text}'")
    def add_positive_indicator(self, text: str) -> 'AudiencesPage':
        """Добавление позитивного индикатора в форму"""
        self.form.add_positive_indicator(text)
        return self

    @allure.step("Добавить негативный индикатор: '{text}'")
    def add_negative_indicator(self, text: str) -> 'AudiencesPage':
        """Добавление негативного индикатора в форму"""
        self.form.add_negative_indicator(text)
        return self

    @allure.step("Проверить наличие позитивного индикатора: '{text}'")
    def is_positive_indicator_visible(self, text: str) -> bool:
        """Проверка наличия позитивного индикатора в форме"""
        return self.form.is_positive_indicator_visible(text)

    @allure.step("Проверить наличие негативного индикатора: '{text}'")
    def is_negative_indicator_visible(self, text: str) -> bool:
        """Проверка наличия негативного индикатора в форме"""
        return self.form.is_negative_indicator_visible(text)

    @allure.step("Удалить индикатор: '{text}'")
    def delete_indicator(self, text: str) -> 'AudiencesPage':
        """Удаление индикатора из формы"""
        self.form.delete_indicator(text)
        return self

    @allure.step("Удалить все индикаторы")
    def delete_all_indicators(self) -> 'AudiencesPage':
        """Удаление всех индикаторов из формы"""
        self.form.delete_all_indicators()
        return self

    @allure.step("Получить значение поля 'Название'")
    def get_form_name_value(self) -> str:
        """Получение текущего значения поля названия в форме"""
        return self.form.get_name_value()

    @allure.step("Заполнить поле 'Название'")
    def fill_audience_name(self, name: str) -> 'AudiencesPage':
        """Заполнение названия аудитории в форме"""
        self.form.fill_name(name)
        return self

    @allure.step("Проверить видимость формы")
    def is_form_visible(self) -> bool:
        """Проверка видимости формы создания/редактирования"""
        return self.form.is_visible

    @allure.step("Сохранить форму")
    def save_form(self) -> 'AudiencesPage':
        """Сохранение формы"""
        self.form.save()
        return self

