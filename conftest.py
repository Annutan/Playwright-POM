"""Конфигурация pytest с фикстурами для Playwright"""
import pytest
import allure
import os
import logging
from playwright.sync_api import Page
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

logger = logging.getLogger(__name__)

# Получаем данные из .env
BASE_URL = os.getenv("BASE_URL")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


# === ХУКИ ДЛЯ СКРИНШОТОВ ПРИ ПАДЕНИИ ===

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания отчета и скриншотов при падении"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = None
        for fixture_name in item.fixturenames:
            if "page" in fixture_name:
                try:
                    page = item.funcargs[fixture_name]
                    break
                except KeyError:
                    continue

        if page and hasattr(page, 'screenshot'):
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name=f"screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Тест '{item.name}' упал. Скриншот сохранен в отчете Allure.")


# === FIXTURES ===

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Конфигурация контекста браузера для всех тестов"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Аргументы запуска браузера"""
    return {
        **browser_type_launch_args,
        "headless": HEADLESS,
        "args": ["--start-maximized", "--disable-dev-shm-usage"]
    }


def _perform_login_with_locators(page: Page) -> bool:
    """Авторизация с использованием локаторов"""
    logger.info("Выполняю авторизацию с использованием локаторов")

    try:
        from test_frontend_settings.locators.auth_locators import AuthLocators
        from test_frontend_settings.locators.main_page_locators import MainPageLocators

        # Проверяем, не авторизованы ли мы уже
        picture_day = page.locator(MainPageLocators.PICTURE_DAY)
        if picture_day.is_visible(timeout=2000):
            logger.info("Уже авторизован")
            return True

        # Ждем форму авторизации
        email_field = page.locator(AuthLocators.EMAIL_FIELD)
        email_field.wait_for(state="visible", timeout=5000)

        # Заполняем поля
        email_field.fill(LOGIN)

        password_field = page.locator(AuthLocators.PASSWORD_FIELD)
        password_field.fill(PASSWORD)

        login_button = page.locator(AuthLocators.LOGIN_BUTTON)
        login_button.click()

        # Ждем успешной авторизации
        page.wait_for_load_state("domcontentloaded")
        picture_day.wait_for(state="visible", timeout=10000)

        logger.info("Авторизация успешна")
        return True

    except Exception as e:
        logger.error(f"Ошибка при авторизации: {e}")
        try:
            allure.attach(
                page.screenshot(),
                name="auth_error_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass
        return False


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """Фикстура для авторизованной страницы"""
    logger.info("Создание авторизованной страницы")

    # Убеждаемся что страница жива
    try:
        page.evaluate("1")
    except:
        logger.error("Страница закрыта, создаем новую")
        from playwright.sync_api import sync_playwright
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

    page.set_default_timeout(15000)

    try:
        logger.info(f"Переход на {BASE_URL}")
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(500)

        # Проверяем, не авторизованы ли мы уже
        from test_frontend_settings.locators.main_page_locators import MainPageLocators
        picture_day = page.locator(MainPageLocators.PICTURE_DAY)

        if picture_day.is_visible(timeout=1000):
            logger.info("Уже авторизован")
            yield page
            return

        logger.info("Требуется авторизация")
        if not _perform_login_with_locators(page):
            pytest.fail("Не удалось выполнить авторизацию")

    except Exception as e:
        logger.error(f"Ошибка при создании авторизованной страницы: {e}")
        pytest.fail(f"Ошибка инициализации: {str(e)}")

    yield page


@pytest.fixture
def audiences_page(authenticated_page: Page):
    """Фикстура для страницы аудиторий"""
    logger.info("Создание фикстуры audiences_page")

    try:
        from test_frontend_settings.locators.navigation_locators import NavigationLocators
        from test_frontend_settings.locators.audiences_locators import AudiencesPageLocators

        logger.info("Переход в Настройки → Аудитории")

        # Делаем скриншот перед навигацией
        allure.attach(
            authenticated_page.screenshot(),
            name="before_navigation",
            attachment_type=allure.attachment_type.PNG
        )

        # Кликаем на Настройки
        settings_btn = authenticated_page.locator(NavigationLocators.TOOLBAR_SETTINGS)
        settings_btn.wait_for(state="visible", timeout=15000)
        settings_btn.click()
        logger.info("Клик на 'Настройки'")

        # Ждем появления подменю
        authenticated_page.wait_for_timeout(1000)

        # Кликаем на Аудитории
        audiences_btn = authenticated_page.locator(NavigationLocators.SUBMENU_AUDIENCES)
        audiences_btn.wait_for(state="visible", timeout=10000)
        audiences_btn.click()
        logger.info("Клик на 'Аудитории'")

        # Ждем загрузки страницы аудиторий
        add_button = authenticated_page.locator(AudiencesPageLocators.ADD_BUTTON)
        add_button.wait_for(state="visible", timeout=20000)

        # Делаем скриншот после навигации
        allure.attach(
            authenticated_page.screenshot(),
            name="after_navigation",
            attachment_type=allure.attachment_type.PNG
        )

        logger.info("Страница аудиторий успешно загружена")

        from test_frontend_settings.pages.audiences_page import AudiencesPage
        return AudiencesPage(authenticated_page)

    except Exception as e:
        logger.error(f"Ошибка при переходе на страницу аудиторий: {e}")
        allure.attach(
            authenticated_page.screenshot(),
            name="navigation_error_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        pytest.fail(f"Не удалось перейти на страницу аудиторий: {str(e)}")


@pytest.fixture
def test_data():
    """Фикстура для тестовых данных"""
    from test_frontend_settings.data.audiences_data import TestData
    return TestData


# === ДОПОЛНИТЕЛЬНЫЕ ХУКИ ===

def pytest_configure(config):
    """Конфигурация pytest - регистрация кастомных маркеров"""
    markers = [
        "audiences: Tests for audiences module",
        "smoke: Smoke tests",
        "regression: Regression tests",
        "critical: Critical functionality",
        "crud: CRUD operation tests",
        "dependency: Test dependencies"
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)


def pytest_sessionstart(session):
    """Действия при начале сессии тестов"""
    logger.info("=== Начало сессии тестов ===")
    os.makedirs("allure-results", exist_ok=True)

    if not LOGIN or not PASSWORD:
        logger.warning("Логин или пароль не установлены в .env файле!")


def pytest_sessionfinish(session, exitstatus):
    """Действия при завершении сессии тестов"""
    logger.info(f"=== Завершение сессии тестов. Статус: {exitstatus} ===")
