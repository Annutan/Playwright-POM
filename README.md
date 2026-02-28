# Содержание

1. Общая информация
2. Структура проекта
3. Технологический стек
4. Архитектура проекта
5. Установка и настройка
6. Переменные окружения (.env)
7. Запуск тестов
8. Allure отчетность
9. Логирование
10. CI/CD интеграция
11. Ссылки на разделы

# Общая информация
Проект автоматизированного тестирования web-приложения "mAi". Фреймворк построен на базе Playwright с использованием паттернов Page Object Model (POM), Page Component и Page Factory.

**Основные возможности:**

- Автоматизация CRUD операций для раздела "Аудитории"
- Много1уровневая архитектура для переиспользования кода
- Поддержка синхронного API Playwright
- Генерация подробных отчетов Allure
- Кроссплатформенность (Windows/macOS/Linux)
- Параллельный запуск тестов
- Ротация логов

# Структура проекта

test_frontend_settings/

| Путь к файлу | Файл | Описание |
| --- | --- | --- |
| ├── 📁 data/  |  | Тестовые данные |
| │   └──  | audiences_data.py | Данные для тестов аудиторий |
| │ | | |
| ├── 📁 locators/ |  | Локаторы (XPath/CSS) |
| │   ├──| auth_locators.py | Локаторы авторизации |
| │   ├── | audiences_locators.py | Локаторы аудиторий |
| │   ├── | main_page_locators.py | Локаторы главной страницы |
| │   └── | navigation_locators.py | Локаторы навигации |
| │ |  |  |
| ├── 📁 elements/ |  | Page Factory - базовые элементы |
| │   ├── | base_element.py | Базовый класс с общими методами |
| │   ├── | button_element.py | Кнопки |
| │   ├── | input_element.py | Поля ввода |
| │   ├── | link_element.py | Ссылки |
| │   ├── | text_element.py | Текстовые элементы |
| │   ├── | table_element.py | Элементы таблицы |
| │   └── | modal_element.py | Элементы модального окна |
| │ |  |  |
| ├── 📁 components/  |  | Page Component - переиспользуемые компоненты |
| │   ├── | base_component.py | Базовый компонент |
| │   ├── | form_component.py | Форма |
| │   ├── | modal_component.py | Модальное окно подтверждения |
| │   ├── | search_component.py | Поиск |
| │   └── | table_component.py | Таблица |
| │ |  |  |
| ├── 📁 pages/  |  | Page Object - страницы приложения |
| │   ├── | base_page.py | Базовая страница |
| │   ├── | login_page.py | Страница авторизации |
| │   ├── | navigation_page.py | Навигация по разделам |
| │   └── | audiences_page.py | Страница аудиторий |
| │ |  |  |
| ├── 📁 tests/  |  | Тестовые сценарии |
| │   └── | test_aud_crud_001.py | CRUD тест aud-crud-001 |
| │ |  |  |
| ├── 📁 utils/  |  | Вспомогательные утилиты |
| │   ├── | allure_helper.py | Помощники для Allure |
| │   ├── | logger.py | Настройка логирования |
| │   └── | logger_confug.py | Конфигурация логгера |
| │ |  |  |
| ├── 📁 logs/ |  | Лог-файлы (создается автоматически) |
| │   └── | autotests.log | Основной лог с ротацией |
| │ |  |  |
| ├── | conftest.py | Фикстуры Pytest |
| ├── | pytest.ini | Конфигурация Pytest |
| ├── | requirements.txt | Зависимости |
| ├── | setup.py | Установка пакета |
| └── | .env | Переменные окружения (не в git) |

# Технологический стек

| Компонент | Версия | Назначение |
| --- | --- | --- |
| Python| 3.10+ | Язык программирования |
| Pytest| 8.3.5+ | Тестовый фреймворк |
| Playwright | 1.45.0+ | Автоматизация браузера |
| Allure | 2.13.0+ | Отчетность |
| python-dotenv | 1.0.0+ | Переменные окружения |
| pytest-xdist | 3.5.0+ | Параллельный запуск |
| pytest-html | 4.1.0+ | HTML отчеты |
| Faker | 20.0.0+ | Генерация тестовых данных |

# Архитектура проекта
Проект использует многоуровневую архитектуру:

1. Page Factory (elements/)

    - Базовые элементы, инкапсулирующие взаимодействие с конкретными типами UI-компонентов:
    - ButtonElement - работа с кнопками
    - InputElement - работа с полями ввода
    - TableElement - работа с таблицами
    - ModalElement - работа с модальными окнами

2. Page Component (components/)

Переиспользуемые составные компоненты, построенные из базовых элементов:
    
    - BaseComponent - базовые компоненты
    - FormComponent - форма создания/редактирования
    - TableComponent - таблица с данными
    - SearchComponent - поиск
    - ModalComponent - модальное окно с логикой подтверждения

3. Page Object (pages/)

Страницы приложения, объединяющие компоненты в бизнес-логику:

    - LoginPage - страница авторизации
    - AudiencesPage - страница управления аудиториями
    - NavigationPage - навигация между разделами

4. Tests (tests/)

Тестовые сценарии с Allure-шагами:

    - test_aud_crud_001.py - полный CRUD цикл

# Установка и настройка

1. Клонирование репозитория

    `git clone `

2. Создание виртуального окружения

    ```
    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

    ```
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Установка зависимостей

    `pip install -r requirements.txt`

4. Установка браузеров Playwright

    ```
    # Или только нужных
    playwright install chromium
    playwright install firefox
    playwright install webkit
    ```
    
5. Создание файла .env

Создайте файл .env в корневой папке проекта (см. Переменные окружения).

# Переменные окружения (.env)
Шаблон .env

    ```
    # Конфигурация окружения
    BASE_URL=сайт
    LOGIN=логин
    PASSWORD=пароль

    # Настройки браузера
    BROWSER=chrome
    HEADLESS=false    # true для запуска без UI
    TIMEOUT=15
    PAGE_LOAD_TIMEOUT=30

    # Настройки отчетности
    ALLURE_RESULTS_DIR=allure-results
    SCREENSHOTS_DIR=screenshots
    ```
    
**Расшифровка переменных `.env`**

| Переменная | Значение по умолчанию | Описание |
| --- | --- | --- | 
| `BASE_URL` | - | Базовый URL приложения |
| `LOGIN` | - | Логин для авторизации |
| `PASSWORD` | - | Пароль для авторизации |
| `BROWSER` | `chrome` | Браузер для тестов | 
| `HEADLESS` | `false` | Режим браузера (`true` - без GUI, `false` - с GUI) |
| `TIMEOUT` | `15` | Таймаут операций (секунд) | 
| `PAGE_LOAD_TIMEOUT` | `30` | Таймаут загрузки страницы (секунд) | 
| `ALLURE_RESULTS_DIR` | `allure-results` | Папка для Allure отчетов | 
| `SCREENSHOTS_DIR` | `screenshots` | Папка для скриншотов |

# Конфигурация Pytest (pytest.ini)
    ```
    [pytest]
    testpaths = tests
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*

    # Параметры запуска
    addopts =
        -v
        --strict-markers
        --alluredir=allure-results
        --disable-warnings
        --tb=short

    # Маркеры (должны совпадать с conftest.py)
    markers =
        smoke: Smoke tests
        regression: Regression tests
        critical: Critical functionality
        audiences: Tests for audiences module
        crud: CRUD operation tests    
        dependency: Test dependencies

    # Настройки логгирования
    log_cli = true
    log_cli_level = INFO
    log_cli_format = %(asctime)s [%(levelname)s] %(name)s: %(message)s
    log_cli_date_format = %Y-%m-%d %H:%M:%S

    # Настройки playwright
    playwright_browsers = chromium
    ```
**Расшифровка переменных `pytest.ini`**

| Параметр | Значение | Описание |
| --- | --- | --- | 
| `testpaths` | `tests` | Директория с тестами |
| `python_files` | `test_*.py` | Маска для файлов с тестами |
| `python_classes` | `Test*` | Классы с тестами должны начинаться с Test |
| `python_functions` | `test_*` | Функции тестов должны начинаться с test_ |
| `-v` | - | Подробный вывод |
| `--strict-markers` | - | Строгая проверка маркеров |
| `--alluredir` | `allure-results` | Директория для Allure отчетов |
| `--disable-warnings` | - | Отключение предупреждений |
| `--tb=short` | - | Короткий вывод traceback |  

# Запуск тестов
**Основные команды**

Запуск всех тестов

    `pytest`

Запуск конкретного теста

    ```
    # Тест AUD-CRUD-001
    pytest tests/test_aud_crud_001.py -v
    ```
    
Запуск с маркером

    ```
    # Тесты с маркером audiences
    pytest -m audiences -v
    
    # Smoke тесты
    pytest -m smoke -v

    # Тесты с маркером crud
    pytest -m crud -v
   
    # Критические тесты
    pytest -m critical -v
    
    # Критические тесты аудиторий
    pytest -m "critical and audiences" -v

    # Smoke или CRUD тесты
    pytest -m "smoke or crud" -v
    ```
Запуск с подробным выводом

    `pytest -v -s --log-cli-level=INFO`

**Параллельный запуск**

    ```
    # Запуск в 4 потока
    pytest -n 4
  
    # Запуск в количество потоков = количество CPU
    pytest -n auto
    ```
    
**Генерация HTML отчета**

    `pytest --html=report.html`

**Режимы браузера**

Видимый режим (с GUI)

    ```
    # Через .env
    HEADLESS=false pytest
    ```

**Невидимый режим (headless)**

    ```
    # Через .env
    HEADLESS=true pytest
    ```

**Выбор браузера**

    ```
    # Chromium (по умолчанию)
    pytest --browser=chromium
   
    # Firefox
    pytest --browser=firefox
   
    # WebKit (Safari)
    pytest --browser=webkit
    
    # Несколько браузеров
    pytest --browser=chromium --browser=firefox
    ```
    
**Комбинированные команды**

    ```
    # Запуск тестов аудиторий в 2 потока с отчетом Allure
    pytest -m audiences -n 2 --alluredir=allure-results
   
    # Запуск конкретного теста в Firefox с HTML отчетом
    pytest tests/test_aud_crud_001.py --browser=firefox --html=report.html
    ```
    
# Allure отчетность
**Установка Allure**

Windows

    ```
    # Через пакетный менеджер scoop
    scoop install allure

    # Через winget
    winget install allure

    # Или скачайте с официального сайта
    # https://github.com/allure-framework/allure2/releases
    ```

macOS

    `brew install allure`

Linux

    ```
    sudo apt-add-repository ppa:qameta/allure
    sudo apt-get update
    sudo apt-get install allure
    ```
    
**Генерация и просмотр отчетов**

1. Запуск тестов с сохранением результатов

    `pytest --alluredir=allure-results`

2. Просмотр отчета в браузере

    `allure serve allure-results`

3. Генерация статического отчета

    ```
    # Генерация
    allure generate allure-results -o allure-report --clean

    # Открытие
    allure open allure-report
    ```
    
**Особенности Allure в проекте**

-  Скриншоты только при падении тестов - экономия места
-  Шаги с аннотацией @allure.step - детальная трассировка
-  Прикрепление логов - текстовые вложения с проверками
-  JSON вложения - структурированные данные
-  Флаги выполнения - flag_clean, flag_create и т.д.
-  Итоговый отчет - сводка по всем алгоритмам

**Пример Allure-шага в тесте**

    ```
    @allure.step("Проверить создание аудитории в таблице")
    def check_audience_created(self, name: str):
        row_count = self.table.row_count
        assert row_count == 1, f"Ожидалась 1 запись, найдено {row_count}"
        allure.attach(
            f"Аудитория '{name}' успешно создана",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )
    ```
# Скриншоты при падении
Скриншоты сохраняются в директорию SCREENSHOTS_DIR (из .env) и также прикрепляются к Allure отчету. 
   
# Логирование
**Настройка логгера**

Логирование настроено в utils/logger.py и utils/logger_confug.py.

**Особенности логирования**

- Ротация логов: 10 МБ на файл, 5 файлов бэкапа
- Директория: logs/autotests.log
- Уровни: DEBUG, INFO, WARNING, ERROR
- Формат: 2026-02-13 16:58:38 | INFO | component | Сообщение

**Пример логов**

    ```
    text
    2026-02-13 16:58:38 | INFO | form_component | Заполняю название: 'TestAudienceBasic'
    2026-02-13 16:58:38 | INFO | input_element | Очищаю поле 'Название'
    2026-02-13 16:58:38 | INFO | input_element | Заполняю поле 'Название': 'TestAudienceBasic'
    2026-02-13 16:58:39 | INFO | form_component | Сохраняю форму
    2026-02-13 16:58:39 | INFO | form_component | Клик по кнопке 'Сохранить' выполнен
    2026-02-13 16:58:39 | INFO | form_component | Форма успешно закрылась
    ```
    
**Просмотр логов в реальном времени**

    ```
    # Во время запуска тестов
    pytest -v -s --log-cli-level=INFO

    # Просмотр лог-файла
    tail -f logs/autotests.log  # Linux/macOS
    Get-Content logs\autotests.log -Wait  # PowerShell
    ```
    
# Ссылки на разделы

- [Утилиты](https://github.com/Annutan/Playwright-POM/tree/main/utils)
- [Фикстуры](https://github.com/Annutan/Playwright-POM/blob/main/conftest.py)
- [Настройки Pytest](https://github.com/Annutan/Playwright-POM/blob/main/pytest.ini)
- [Основные тесты](https://github.com/Annutan/Playwright-POM/tree/main/tests) 
- [Документация](https://github.com/Annutan/Playwright-POM/tree/main/Documents)

# Маркеры тестов

Маркер | Назначение | Пример использования
-- | -- | --
smoke | Быстрая проверка критического функционала | pytest -m smoke
regression | Полная регрессионная проверка | pytest -m regression
critical | Критически важные тесты | pytest -m critical
audiences | Тесты модуля аудиторий | pytest -m audiences
crud | Тесты CRUD операций | pytest -m crud
dependency | Тесты с зависимостями | pytest -m dependency

# Полезные команды для быстрого старта:
    ```
    # Быстрая установка
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    playwright install

    # Быстрый запуск теста
    pytest tests/test_aud_crud_001.py -v --alluredir=allure-results
    allure serve allure-results
    ```
    

