"""Page Object для навигации по приложению"""
import allure
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from ..elements.button_element import ButtonElement
from ..elements.base_element import BaseElement
from ..locators.navigation_locators import NavigationLocators
from ..locators.main_page_locators import MainPageLocators
import logging

logger = logging.getLogger(__name__)


class NavigationPage:
    """Страница для навигации между разделами"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

        # Элементы навигации
        self.toolbar_settings = ButtonElement(
            self.page.locator(NavigationLocators.TOOLBAR_SETTINGS),
            name="меню 'Настройки'"
        )

        # Элементы подменю
        self.submenu_audiences = ButtonElement(
            self.page.locator(NavigationLocators.SUBMENU_AUDIENCES),
            name="подменю 'Аудитории'"
        )

        self.submenu_thematics = ButtonElement(
            self.page.locator(NavigationLocators.SUBMENU_THEMATICS),
            name="подменю 'Тематики'"
        )

        self.submenu_channels = ButtonElement(
            self.page.locator(NavigationLocators.SUBMENU_CHANNELS),
            name="подменю 'Каналы'"
        )

    @allure.step("Перейти в раздел 'Настройки'")
    def go_to_settings(self) -> 'NavigationPage':
        """Переход в раздел Настройки"""
        self.logger.info("Перехожу в раздел 'Настройки'")

        # Ждем видимости и кликаем
        self.toolbar_settings.wait_for_visible(timeout=10000)
        self.toolbar_settings.click()

        # Ждем появления подменю
        self.page.wait_for_timeout(1000)  # Небольшая пауза для анимации

        return self

    @allure.step("Перейти в подраздел 'Аудитории'")
    def go_to_audiences(self) -> 'NavigationPage':
        """Переход в подраздел Аудитории"""
        self.logger.info("Перехожу в подраздел 'Аудитории'")

        # 1. Сначала открываем настройки
        self.go_to_settings()

        # 2. Ждем появления подменю
        self.page.wait_for_timeout(1000)

        # 3. Убеждаемся, что кнопка Аудитории видима
        self.submenu_audiences.wait_for_visible(timeout=10000)

        # 4. Сохраняем URL до клика
        before_url = self.page.url
        self.logger.info(f"URL до клика на Аудитории: {before_url}")

        # 5. Кликаем на Аудитории
        self.submenu_audiences.click()

        # 6. Ждем изменения URL или загрузки страницы
        self.page.wait_for_timeout(3000)

        # 7. Проверяем, что URL изменился (должен содержать audiences)
        after_url = self.page.url
        self.logger.info(f"URL после клика на Аудитории: {after_url}")

        # 8. Если URL не изменился или содержит thematics - что-то пошло не так
        if "thematics" in after_url:
            self.logger.error("Попали на страницу Тематики вместо Аудиторий!")
            # Пробуем еще раз
            self.submenu_audiences.click()
            self.page.wait_for_timeout(3000)
            after_url = self.page.url
            self.logger.info(f"URL после повторного клика: {after_url}")

        return self

    @allure.step("Перейти в подраздел 'Тематики'")
    def go_to_thematics(self) -> 'NavigationPage':
        """Переход в подраздел Тематики"""
        self.logger.info("Перехожу в подраздел 'Тематики'")

        self.go_to_settings()
        self.submenu_thematics.wait_for_visible(timeout=10000)
        self.submenu_thematics.click()
        self.page.wait_for_timeout(2000)

        return self

    @allure.step("Перейти в подраздел 'Каналы'")
    def go_to_channels(self) -> 'NavigationPage':
        """Переход в подраздел Каналы"""
        self.logger.info("Перехожу в подраздел 'Каналы'")

        self.go_to_settings()
        self.submenu_channels.wait_for_visible(timeout=10000)
        self.submenu_channels.click()
        self.page.wait_for_timeout(2000)

        return self

    @allure.step("Проверить что мы на главной странице")
    def verify_on_main_page(self) -> bool:
        """Проверка что мы на главной странице"""
        self.logger.info("Проверяю что мы на главной странице")

        picture_day_element = BaseElement(
            self.page.locator(MainPageLocators.PICTURE_DAY),
            "Элемент 'Картина дня'"
        )

        return picture_day_element.is_visible(timeout=5000)