"""Компонент формы аудитории"""
import allure
from playwright.sync_api import Page
from ..elements.input_element import InputElement
from ..elements.button_element import ButtonElement
from ..elements.base_element import BaseElement
from .base_component import BaseComponent
import logging

logger = logging.getLogger(__name__)


class FormComponent(BaseComponent):
    """Компонент формы аудитории"""

    def __init__(self, page: Page, form_locators, name: str = "форма"):
        super().__init__(page, None, name)
        self.locators = form_locators

        # === ЭЛЕМЕНТЫ ФОРМЫ ===

        # Поле названия
        self.name_input = InputElement(
            page.locator(form_locators.NAME_INPUT),
            name=f"{self.name} - поле 'Название'"
        )

        # Поле ввода индикаторов
        self.indicator_input = InputElement(
            page.locator(form_locators.INDICATOR_INPUT),
            name=f"{self.name} - поле ввода индикаторов"
        )

        # Кнопки добавления индикаторов
        self.add_positive_button = ButtonElement(
            page.locator(form_locators.ADD_POSITIVE_BTN),
            name=f"{self.name} - кнопка добавления позитивного индикатора"
        )

        self.add_negative_button = ButtonElement(
            page.locator(form_locators.ADD_NEGATIVE_BTN),
            name=f"{self.name} - кнопка добавления негативного индикатора"
        )

        # Кнопки формы
        self.save_button = ButtonElement(
            page.locator(form_locators.SAVE_BUTTON),
            name=f"{self.name} - кнопка 'Сохранить'"
        )

        self.cancel_button = ButtonElement(
            page.locator(form_locators.CANCEL_BUTTON),
            name=f"{self.name} - кнопка 'Отмена'"
        )

    # === МЕТОДЫ ДЛЯ РАБОТЫ С НАЗВАНИЕМ ===

    @allure.step("Заполнить название: '{name}'")
    def fill_name(self, name: str) -> 'FormComponent':
        """Заполнение названия аудитории"""
        logger.info(f"Заполняю название: '{name}'")
        self.name_input.clear_and_fill(name)
        return self

    @allure.step("Получить значение поля 'Название'")
    def get_name_value(self) -> str:
        """Получение текущего значения поля названия"""
        try:
            # Ждем видимости поля
            self.name_input.wait_for_visible(timeout=3000)
            # Получаем значение
            value = self.name_input.get_value()
            logger.info(f"Значение поля 'Название': '{value}'")
            return value
        except Exception as e:
            logger.error(f"Ошибка при получении значения поля 'Название': {e}")
            return ""

    @allure.step("Очистить поле 'Название'")
    def clear_name(self) -> 'FormComponent':
        """Очистка поля названия"""
        self.name_input.clear()
        return self

    # === МЕТОДЫ ДЛЯ РАБОТЫ С ИНДИКАТОРАМИ ===

    @allure.step("Ввести текст индикатора: '{text}'")
    def fill_indicator_input(self, text: str) -> 'FormComponent':
        """Ввод текста в поле индикатора"""
        logger.info(f"Ввожу текст индикатора: '{text}'")
        self.indicator_input.clear_and_fill(text)
        return self

    @allure.step("Добавить позитивный индикатор: '{text}'")
    def add_positive_indicator(self, text: str) -> 'FormComponent':
        """Добавление позитивного индикатора (зеленый крестик)"""
        logger.info(f"Добавляю позитивный индикатор: '{text}'")
        self.fill_indicator_input(text)
        self.add_positive_button.click()
        self.page.wait_for_timeout(500)  # Небольшая пауза для обновления DOM
        return self

    @allure.step("Добавить негативный индикатор: '{text}'")
    def add_negative_indicator(self, text: str) -> 'FormComponent':
        """Добавление негативного индикатора (красный крестик)"""
        logger.info(f"Добавляю негативный индикатор: '{text}'")
        self.fill_indicator_input(text)
        self.add_negative_button.click()
        self.page.wait_for_timeout(500)
        return self

    @allure.step("Проверить наличие позитивного индикатора: '{text}'")
    def is_positive_indicator_visible(self, text: str) -> bool:
        """Проверка видимости позитивного индикатора по тексту"""
        try:
            locator = self.locators.ADDED_POSITIVE_INDICATOR_TEMPLATE.format(text=text)
            indicator_element = BaseElement(
                self.page.locator(locator),
                name=f"позитивный индикатор '{text}'"
            )
            return indicator_element.is_visible(timeout=3000)
        except Exception as e:
            logger.debug(f"Ошибка при проверке позитивного индикатора: {e}")
            return False

    @allure.step("Проверить наличие негативного индикатора: '{text}'")
    def is_negative_indicator_visible(self, text: str) -> bool:
        """Проверка видимости негативного индикатора по тексту"""
        try:
            locator = self.locators.ADDED_NEGATIVE_INDICATOR_TEMPLATE.format(text=text)
            indicator_element = BaseElement(
                self.page.locator(locator),
                name=f"негативный индикатор '{text}'"
            )
            return indicator_element.is_visible(timeout=3000)
        except Exception as e:
            logger.debug(f"Ошибка при проверке негативного индикатора: {e}")
            return False

    @allure.step("Проверить наличие индикатора (любого типа): '{text}'")
    def is_indicator_visible(self, text: str) -> bool:
        """Проверка видимости индикатора любого типа"""
        # Проверяем оба типа
        return (self.is_positive_indicator_visible(text) or
                self.is_negative_indicator_visible(text))

    @allure.step("Удалить индикатор: '{text}'")
    def delete_indicator(self, text: str) -> 'FormComponent':
        """Удаление индикатора по тексту"""
        logger.info(f"Удаляю индикатор: '{text}'")

        # Проверяем оба типа индикаторов
        for indicator_type, locator_template in [
            ('positive', self.locators.ADDED_POSITIVE_INDICATOR_TEMPLATE),
            ('negative', self.locators.ADDED_NEGATIVE_INDICATOR_TEMPLATE)
        ]:
            try:
                locator = locator_template.format(text=text)
                # Ищем кнопку удаления рядом с индикатором
                delete_button_locator = f"{locator}/ancestor::div[contains(@class, 'item_')]//button"
                delete_button = ButtonElement(
                    self.page.locator(delete_button_locator),
                    name=f"кнопка удаления индикатора '{text}'"
                )

                if delete_button.is_visible(timeout=1000):
                    delete_button.click()
                    self.page.wait_for_timeout(500)

                    # Проверяем что индикатор исчез
                    indicator_element = BaseElement(
                        self.page.locator(locator),
                        name=f"индикатор '{text}'"
                    )
                    if not indicator_element.is_visible(timeout=3000):
                        logger.info(f"Индикатор '{text}' успешно удален")
                        return self
            except Exception as e:
                logger.debug(f"Не удалось удалить {indicator_type} индикатор '{text}': {e}")
                continue

        logger.warning(f"Индикатор '{text}' не найден или не удален")
        return self

    @allure.step("Удалить все индикаторы")
    def delete_all_indicators(self) -> 'FormComponent':
        """Удаление всех индикаторов в форме"""
        logger.info("Удаляю все индикаторы")

        # Ищем все кнопки удаления индикаторов
        delete_buttons_locator = "//div[contains(@class, 'item_')]//button"
        delete_buttons = self.page.locator(delete_buttons_locator)

        count = delete_buttons.count()
        for i in range(count):
            try:
                # Всегда берем первую кнопку, так как после удаления список меняется
                first_button = self.page.locator(delete_buttons_locator).first
                if first_button.is_visible(timeout=1000):
                    first_button.click()
                    self.page.wait_for_timeout(300)
            except Exception as e:
                logger.debug(f"Ошибка при удалении индикатора: {e}")

        return self

    @allure.step("Получить список всех индикаторов")
    def get_all_indicators(self) -> list:
        """Получение списка всех индикаторов в форме"""
        indicators = []

        # Получаем позитивные индикаторы
        positive_locator = "//div[contains(@class, 'item_positive')]//span"
        positive_elements = self.page.locator(positive_locator)

        for i in range(positive_elements.count()):
            try:
                text = positive_elements.nth(i).text_content()
                if text:
                    indicators.append({"text": text.strip(), "type": "positive"})
            except:
                pass

        # Получаем негативные индикаторы
        negative_locator = "//div[contains(@class, 'item_negative')]//span"
        negative_elements = self.page.locator(negative_locator)

        for i in range(negative_elements.count()):
            try:
                text = negative_elements.nth(i).text_content()
                if text:
                    indicators.append({"text": text.strip(), "type": "negative"})
            except:
                pass

        logger.info(f"Найдено индикаторов в форме: {len(indicators)}")
        return indicators

    @allure.step("Добавить несколько индикаторов")
    def add_multiple_indicators(self, indicators: list) -> 'FormComponent':
        """
        Добавление нескольких индикаторов
        :param indicators: список словарей [{'text': 'индикатор1', 'type': 'positive'}, ...]
        """
        for indicator in indicators:
            if indicator['type'] == 'positive':
                self.add_positive_indicator(indicator['text'])
            else:
                self.add_negative_indicator(indicator['text'])

        logger.info(f"Добавлено {len(indicators)} индикаторов")
        return self

    # === МЕТОДЫ ДЛЯ РАБОТЫ С КНОПКАМИ ФОРМЫ ===

    @allure.step("Сохранить форму")
    def save(self) -> 'FormComponent':
        """Сохранение формы"""
        logger.info("Сохраняю форму")

        # Проверяем что кнопка видима и кликабельна
        self.save_button.wait_for_visible(timeout=5000)

        # Кликаем по кнопке
        self.save_button.click()
        logger.info("Клик по кнопке 'Сохранить' выполнен")

        # Ждем скрытия формы - недолго, 2 секунды максимум
        try:
            self.name_input.wait_for_hidden(timeout=2000)
            logger.info("Форма успешно закрылась")
        except:
            logger.warning("Форма не закрылась после сохранения за 2 секунды")

        return self

    @allure.step("Отменить создание/редактирование")
    def cancel(self) -> 'FormComponent':
        """Отмена действия"""
        logger.info("Отменяю действие")
        self.cancel_button.click()
        self.page.wait_for_timeout(500)
        return self

    @allure.step("Нажать кнопку 'Сохранить' и дождаться закрытия формы")
    def save_and_wait_close(self, timeout: int = 5000) -> 'FormComponent':
        """Сохранение формы и ожидание ее закрытия"""
        self.save()
        self.wait_for_hidden(timeout)
        return self

    # === МЕТОДЫ ПРОВЕРКИ СОСТОЯНИЯ ФОРМЫ ===

    @property
    def is_visible(self) -> bool:
        """Проверка видимости формы"""
        return self.name_input.is_visible(timeout=2000)

    @property
    def is_hidden(self) -> bool:
        """Проверка скрытия формы"""
        return not self.is_visible

    @allure.step("Ожидать видимость формы")
    def wait_for_visible(self, timeout: int = 5000) -> bool:
        """Ожидание видимости формы"""
        try:
            self.name_input.wait_for_visible(timeout)
            return True
        except:
            return False

    @allure.step("Ожидать скрытие формы")
    def wait_for_hidden(self, timeout: int = 5000) -> bool:
        """Ожидание скрытия формы"""
        try:
            self.name_input.wait_for_hidden(timeout)
            return True
        except:
            return False

    @allure.step("Проверить что форма содержит данные")
    def has_data(self) -> bool:
        """Проверка что форма содержит какие-то данные"""
        name_value = self.get_name_value()
        indicators = self.get_all_indicators()

        return bool(name_value) or bool(indicators)

    @allure.step("Проверить что форма пустая")
    def is_empty(self) -> bool:
        """Проверка что форма не содержит данных"""
        return not self.has_data()

    @allure.step("Проверить наличие индикатора в таблице")
    def verify_indicator_in_table(self, audience_name: str, indicator_text: str) -> bool:
        """Проверка наличия индикатора в строке таблицы"""
        try:
            # Ищем строку с названием аудитории
            row_locator = f"//div[contains(@class, 'AudiencesTable_audiencesTable__row_')][.//a[text()='{audience_name}']]"
            row = self.page.locator(row_locator)

            if row.is_visible():
                # Проверяем наличие индикатора в строке
                indicator_locator = f".//span[contains(text(), '{indicator_text}')]"
                indicator = row.locator(indicator_locator)
                return indicator.is_visible(timeout=2000)
        except Exception as e:
            logger.debug(f"Ошибка при проверке индикатора в таблице: {e}")

        return False