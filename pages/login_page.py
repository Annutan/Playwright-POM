"""Page Object для страницы авторизации на Playwright"""
import allure
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from .base_page import BasePage
from ..elements.input_element import InputElement
from ..elements.button_element import ButtonElement
from ..elements.base_element import BaseElement
from ..locators.auth_locators import AuthLocators
from ..locators.main_page_locators import MainPageLocators
import logging
import os

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Страница авторизации"""

    def __init__(self, page: Page):
        super().__init__(page)

        self.base_url = os.getenv("BASE_URL", "https://assist24.tech/app")

        # Элементы страницы
        self.email_field = InputElement(
            self.page.locator(AuthLocators.EMAIL_FIELD),
            name="поле 'Email'"
        )
        self.password_field = InputElement(
            self.page.locator(AuthLocators.PASSWORD_FIELD),
            name="поле 'Пароль'"
        )
        self.login_button = ButtonElement(
            self.page.locator(AuthLocators.LOGIN_BUTTON),
            name="кнопка 'Войти'"
        )

    @allure.step("Открыть страницу авторизации")
    def open(self, force: bool = False) -> 'LoginPage':
        """
        Открытие страницы авторизации
        :param force: Принудительно перезагрузить страницу, даже если уже авторизованы
        """
        # Проверяем, не авторизованы ли мы уже
        try:
            if not force:
                # Проверяем, есть ли элемент "Картина дня"
                picture_day = BaseElement(
                    self.page.locator(MainPageLocators.PICTURE_DAY),
                    "Элемент 'Картина дня'"
                )
                if picture_day.is_visible(timeout=2000):
                    logger.info("Уже авторизованы, пропускаем открытие страницы")
                    return self
        except:
            pass

        # Если не авторизованы или force=True - открываем страницу
        self.navigate(self.base_url)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)
        logger.info(f"Страница авторизации загружена: {self.page.url}")
        return self

    @allure.step("Заполнить поле email: '{email}'")
    def fill_email(self, email: str) -> 'LoginPage':
        """Заполнение поля email"""
        logger.info(f"Заполняю email: '{email}'")

        # Проверяем что мы на странице авторизации
        self.wait_for_login_form()

        try:
            self.email_field.clear_and_fill(email)
        except PlaywrightTimeoutError:
            logger.error("Не удалось найти поле email")
            # Делаем скриншот для отладки
            allure.attach(
                self.page.screenshot(),
                name="email_field_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise
        return self

    @allure.step("Заполнить поле пароль")
    def fill_password(self, password: str) -> 'LoginPage':
        """Заполнение поля пароль"""
        logger.info("Заполняю пароль")

        self.wait_for_login_form()

        try:
            self.password_field.clear_and_fill(password)
        except PlaywrightTimeoutError:
            logger.error("Не удалось найти поле пароля")
            allure.attach(
                self.page.screenshot(),
                name="password_field_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise
        return self

    @allure.step("Нажать кнопку 'Войти'")
    def click_login(self) -> 'LoginPage':
        """Клик по кнопке входа"""
        logger.info("Нажимаю кнопку 'Войти'")

        self.wait_for_login_form()

        try:
            self.login_button.click()
        except PlaywrightTimeoutError:
            logger.error("Не удалось найти кнопку входа")
            allure.attach(
                self.page.screenshot(),
                name="login_button_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise
        return self

    @allure.step("Ожидать появления формы авторизации")
    def wait_for_login_form(self, timeout: int = 10000) -> 'LoginPage':
        """Ожидание появления формы авторизации"""
        logger.info("Ожидаю появления формы авторизации")
        self.email_field.wait_for_visible(timeout)
        return self

    @allure.step("Выполнить авторизацию")
    def perform_login(self, email: str, password: str) -> 'LoginPage':
        """Выполнение авторизации"""
        logger.info(f"Выполняю авторизацию для: {email}")

        # Проверяем, не авторизованы ли мы уже
        if self.verify_login_success(timeout=2000):
            logger.info("Уже авторизованы, пропускаем авторизацию")
            return self

        # Ждем появления формы логина (уменьшаем таймаут)
        self.wait_for_login_form(timeout=5000)

        # Заполняем поля (убираем лишние ожидания)
        self.email_field.clear_and_fill(email)
        self.password_field.clear_and_fill(password)
        self.login_button.click()

        # Ждем загрузки главной страницы (уменьшаем таймаут)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)  # Уменьшаем с 2000 до 1000

        return self

    @allure.step("Проверить успешность авторизации")
    def verify_login_success(self, timeout: int = 10000) -> bool:
        """Проверка успешной авторизации с возможностью кастомизации таймаута"""
        self.logger.info(f"Проверяю успешность авторизации (таймаут: {timeout}мс)")

        try:
            picture_day_element = BaseElement(
                self.page.locator(MainPageLocators.PICTURE_DAY),
                "Элемент 'Картина дня'"
            )

            is_visible = picture_day_element.is_visible(timeout=timeout)
            self.logger.info(f"Элемент 'Картина дня' виден: {is_visible}")

            return is_visible
        except Exception as e:
            self.logger.error(f"Ошибка при проверке авторизации: {e}")
            return False

    @allure.step("Проверить что мы на странице авторизации")
    def is_login_page(self) -> bool:
        """Проверка, что текущая страница - страница авторизации"""
        try:
            return self.email_field.is_visible(timeout=3000)
        except:
            return False