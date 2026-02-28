"""Локаторы для авторизации"""


class AuthLocators:
    """Локаторы страницы авторизации"""

    EMAIL_FIELD = "//input[@name='email']"
    PASSWORD_FIELD = "//input[@name='password']"
    LOGIN_BUTTON = "//button/span[text()='Войти']"