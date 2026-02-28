"""Тест AUD-CRUD-001: Базовый CRUD цикл аудитории.
Соответствует документации AUD-CRUD-001.docx
"""
import allure
import pytest
import logging
from test_frontend_settings.data.audiences_data import TestData
from test_frontend_settings.pages.audiences_page import AudiencesPage
from test_frontend_settings.pages.navigation_page import NavigationPage

logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def test_flags():
    """Фикстура для хранения флагов между тестами"""
    return {
        'flag_clean': None,
        'flag_create': None,
        'flag_edit': None,
        'flag_delete_cancel': None,
        'flag_delete_confirm': None,
        'flag_deleted': None
    }


@allure.feature("Аудитории")
@allure.story("AUD-CRUD-001")
@allure.title("Базовый CRUD цикл аудитории")
@allure.description("""
    Тест проверяет полный цикл CRUD операций для аудиторий:
    1. Очистка тестовых данных (если аудитория уже существует)
    2. Создание аудитории с обязательными полями
    3. Редактирование названия аудитории
    4. Удаление аудитории (с проверкой отмены и подтверждения)
    
    Выходные данные: флаги успешности каждого алгоритма
""")
@pytest.mark.audiences
@pytest.mark.crud
@pytest.mark.critical
class TestAudienceCRUD001:
    """Тесты CRUD операций для аудиторий (AUD-CRUD-001)"""

    # Флаги для отчета
    flag_clean = None
    flag_create = None
    flag_edit = None
    flag_delete_cancel = None
    flag_delete_confirm = None
    flag_deleted = None

    # === АЛГОРИТМ 1: ОЧИСТКА ТЕСТОВЫХ ДАННЫХ ===

    @allure.title("Алгоритм 1: Предварительная очистка тестовых данных")
    @allure.description("""
        Предусловия:
        - Пользователь авторизован в системе
        - Открыта страница "Настройки" → "Аудитории"
        
        Выходные данные: flag_clean = 1/0
    """)
    def test_algorithm_1_cleanup(self, audiences_page: AudiencesPage, test_flags):
        """Алгоритм 1: Очистка тестовых данных перед началом"""
        test_flags['flag_clean'] = 0

        with allure.step("Проверка текущего URL"):
            current_url = audiences_page.page.url
            logger.info(f"Текущий URL в начале теста: {current_url}")
            allure.attach(
                f"URL: {current_url}",
                name="start_url",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("1.1. Поиск существующей тестовой аудитории"):
            logger.info(f"Поиск аудитории: {TestData.AUDIENCE_BASIC_NAME}")
            audiences_page.search.search(TestData.AUDIENCE_BASIC_NAME)

            allure.attach(
                f"Выполнен поиск: '{TestData.AUDIENCE_BASIC_NAME}'",
                name="Поиск аудитории",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("1.2. Проверка наличия аудитории"):
            if audiences_page.is_audience_present(TestData.AUDIENCE_BASIC_NAME):
                self.flag_clean = 1
                logger.info(f"Аудитория найдена, flag_clean = {self.flag_clean}")

                with allure.step("1.2.1. Инициировать удаление аудитории"):
                    audiences_page.initiate_delete_audience(TestData.AUDIENCE_BASIC_NAME)
                    logger.info("Кнопка удаления нажата")

                with allure.step("1.2.2. Проверить модальное окно подтверждения"):
                    # Используем новый метод из компонента
                    audiences_page.modal.verify_delete_confirmation_modal()

                    allure.attach(
                        "Модальное окно проверено: открыто, текст корректен, кнопки Да/Отмена присутствуют",
                        name="Проверка модального окна",
                        attachment_type=allure.attachment_type.TEXT
                    )

                with allure.step("1.2.3. Подтвердить удаление"):
                    # Подтверждаем удаление
                    audiences_page.modal.confirm()
                    logger.info("Удаление подтверждено")

                    # Ждем закрытия модального окна
                    assert audiences_page.modal.wait_for_close(timeout=5000), "Модальное окно не закрылось"

                    allure.attach(
                        "Удаление подтверждено, модальное окно закрыто",
                        name="Подтверждение удаления",
                        attachment_type=allure.attachment_type.TEXT
                    )

                with allure.step("1.2.4. Дополнительная проверка удаления"):
                    # Снова ищем аудиторию
                    audiences_page.search.search(TestData.AUDIENCE_BASIC_NAME)
                    audiences_page.page.wait_for_timeout(1000)

                    # Проверяем что аудитория удалена
                    is_still_present = audiences_page.is_audience_present(TestData.AUDIENCE_BASIC_NAME, timeout=2000)
                    assert not is_still_present, "Аудитория все еще найдена после удаления"

                    allure.attach(
                        f"Аудитория после удаления: {'найдена' if is_still_present else 'не найдена'}",
                        name="Проверка удаления",
                        attachment_type=allure.attachment_type.TEXT
                    )

            else:
                with allure.step("1.2.1. Аудитория не найдена, очистка поиска"):
                    audiences_page.search.clear_search()
                    test_flags['flag_clean'] = 0

        with allure.step("Выходные данные"):
            allure.attach(
                f"flag_clean = {test_flags['flag_clean']}\n"  # ← заменить
                f"Что означает:\n"
                f"- Если flag_clean = 1: аудитория существовала и была удалена\n"
                f"- Если flag_clean = 0: аудитория не существовала",
                name="Выходные данные алгоритма 1",
                attachment_type=allure.attachment_type.TEXT
            )

        logger.info(f"Алгоритм 1 завершен. flag_clean = {test_flags['flag_clean']}")

    # === АЛГОРИТМ 2: СОЗДАНИЕ АУДИТОРИИ ===

    @allure.title("Алгоритм 2: Создание аудитории с обязательными полями")
    @allure.description("""
        Предусловия:
        - Алгоритм 1 успешно выполнен
        - Аудитория TestAudienceBasic не существует в системе
        - Открыта страница "Настройки" → "Аудитории"
        
        Выходные данные: flag_create = 1/0
    """)
    def test_algorithm_2_create(self, audiences_page: AudiencesPage, test_flags):
        """Алгоритм 2: Создание аудитории с обязательными полями"""

        # Пропускаем тест, если предыдущий не выполнен
        if test_flags['flag_clean'] is None:
            pytest.skip("Алгоритм 1 не выполнен, пропускаем алгоритм 2")

        test_flags['flag_create'] = 0

        with allure.step("2.1. Нажать кнопку 'Добавить аудиторию'"):
            audiences_page.add_button.click()
            assert audiences_page.form.wait_for_visible(), "Форма создания не отображается"

            allure.attach(
                "Форма создания аудитории открыта",
                name="Открытие формы",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2.2. Заполнить поле 'Название'"):
            audiences_page.form.fill_name(TestData.AUDIENCE_BASIC_NAME)
            name_value = audiences_page.form.get_name_value()

            assert name_value == TestData.AUDIENCE_BASIC_NAME, \
                f"Поле названия не заполнено. Ожидалось: {TestData.AUDIENCE_BASIC_NAME}, получено: {name_value}"

            allure.attach(
                f"Поле 'Название' заполнено: '{TestData.AUDIENCE_BASIC_NAME}'",
                name="Заполнение названия",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2.3. Добавить обязательный позитивный индикатор"):
            audiences_page.form.add_positive_indicator(TestData.REQUIRED_INDICATOR)

            allure.attach(
                f"Индикатор добавлен: '{TestData.REQUIRED_INDICATOR}' (позитивный)",
                name="Добавление индикатора",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2.4. Проверить отображение добавленного индикатора"):
            is_indicator_visible = audiences_page.form.is_positive_indicator_visible(
                TestData.REQUIRED_INDICATOR
            )
            assert is_indicator_visible, f"Индикатор '{TestData.REQUIRED_INDICATOR}' не отображается"

            allure.attach(
                f"Индикатор проверен: виден",
                name="Проверка индикатора",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2.5. Нажать кнопку 'Сохранить'"):
            audiences_page.form.save()

            # УЛУЧШЕННОЕ ОЖИДАНИЕ
            # Ждем не просто время, а проверяем, что форма закрылась
            assert audiences_page.form.wait_for_hidden(timeout=5000), "Форма не закрылась после сохранения"

            # Даем время на обновление данных в бэкенде
            audiences_page.page.wait_for_timeout(2000)

            allure.attach(
                "Форма сохранена",
                name="Сохранение формы",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2.6. Проверить создание аудитории в таблице"):
            # Сначала проверим, что поиск работает
            test_search = audiences_page.search.get_value()
            logger.info(f"Текущее значение поиска перед вводом: '{test_search}'")

            # Выполняем поиск
            audiences_page.search.search(TestData.AUDIENCE_BASIC_NAME)

            # Проверяем, что текст применился
            applied_search = audiences_page.search.get_value()
            logger.info(f"Значение поиска после ввода: '{applied_search}'")
            assert applied_search == TestData.AUDIENCE_BASIC_NAME, "Текст поиска не применился"

            # Даем время на фильтрацию
            audiences_page.page.wait_for_timeout(2000)

            # Проверяем количество записей
            row_count = audiences_page.table.row_count
            logger.info(f"Количество записей после поиска: {row_count}")

            assert row_count == 1, f"Ожидалась 1 запись, найдено {row_count}"

            test_flags['flag_create'] = 1

            allure.attach(
                f"Количество записей после создания: {row_count}",
                name="Проверка количества записей",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2.7. Проверить данные созданной аудитории"):
            # Проверка названия
            assert audiences_page.is_audience_present(TestData.AUDIENCE_BASIC_NAME), \
                f"Аудитория '{TestData.AUDIENCE_BASIC_NAME}' не найдена"

            # Проверка статуса (должен быть активен по умолчанию)
            status = audiences_page.get_audience_status(TestData.AUDIENCE_BASIC_NAME)
            assert status, "Аудитория не активна по умолчанию"

            # ПРОВЕРКА ИНДИКАТОРА - ИСПРАВЛЕНО
            row = audiences_page.table.find_row_by_audience_name(TestData.AUDIENCE_BASIC_NAME)
            assert row.contains_text(TestData.REQUIRED_INDICATOR), \
                f"Индикатор '{TestData.REQUIRED_INDICATOR}' не отображается в таблице"

            allure.attach(
                f"Данные аудитории проверены:\n"
                f"- Название: {TestData.AUDIENCE_BASIC_NAME} ✓\n"
                f"- Индикатор: {TestData.REQUIRED_INDICATOR} ✓\n"
                f"- Статус: {'Активна' if status else 'Неактивна'} ✓",
                name="Проверка данных аудитории",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Выходные данные"):
            allure.attach(
                f"flag_create = {test_flags['flag_create']}\n",
                name="Выходные данные алгоритма 2",
                attachment_type=allure.attachment_type.TEXT
            )

        logger.info(f"Алгоритм 2 завершен. flag_create = {test_flags['flag_create']}")

    # === АЛГОРИТМ 3: РЕДАКТИРОВАНИЕ НАЗВАНИЯ ===

    @allure.title("Алгоритм 3: Редактирование названия аудитории")
    @allure.description("""
        Предусловия:
        - Алгоритм 2 успешно выполнен
        - Аудитория TestAudienceBasic создана и отображается в таблице
        - Открыта страница "Настройки" → "Аудитории"
        
        Выходные данные: flag_edit = 1/0
    """)
    def test_algorithm_3_edit(self, audiences_page: AudiencesPage, test_flags):
        """Алгоритм 3: Редактирование названия аудитории"""

        if test_flags['flag_create'] != 1:
            pytest.skip("Алгоритм 2 не выполнен успешно, пропускаем алгоритм 3")

        test_flags['flag_edit'] = 0

        with allure.step("3.1. Найти аудиторию в таблице"):
            audiences_page.search.search(TestData.AUDIENCE_BASIC_NAME)
            assert audiences_page.table.row_count == 1, "Аудитория не найдена для редактирования"

            allure.attach(
                f"Найдена аудитория: '{TestData.AUDIENCE_BASIC_NAME}'",
                name="Поиск аудитории для редактирования",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3.2. Открыть аудиторию для редактирования"):
            audiences_page.open_audience_for_edit(TestData.AUDIENCE_BASIC_NAME)
            assert audiences_page.form.wait_for_visible(), "Форма редактирования не открылась"

            allure.attach(
                "Форма редактирования открыта",
                name="Открытие формы редактирования",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3.3. Проверить текущие данные в форме"):
            # Проверка названия - ИСПРАВЛЕНО
            audiences_page.page.wait_for_timeout(1000)  # Даем время на загрузку
            current_name = audiences_page.form.get_name_value()
            logger.info(f"Текущее название в форме: '{current_name}'")

            assert current_name == TestData.AUDIENCE_BASIC_NAME, \
                f"Текущее название не совпадает. Ожидалось: {TestData.AUDIENCE_BASIC_NAME}, получено: '{current_name}'"

            # Проверка индикатора
            has_indicator = audiences_page.form.is_positive_indicator_visible(
                TestData.REQUIRED_INDICATOR
            )
            assert has_indicator, f"Индикатор '{TestData.REQUIRED_INDICATOR}' не найден в форме"

        with allure.step("3.4. Изменить название аудитории"):
            audiences_page.form.fill_name(TestData.AUDIENCE_EDITED_NAME)

            new_name = audiences_page.form.get_name_value()
            assert new_name == TestData.AUDIENCE_EDITED_NAME, \
                f"Новое название не установлено. Ожидалось: {TestData.AUDIENCE_EDITED_NAME}, получено: {new_name}"

            allure.attach(
                f"Название изменено: '{TestData.AUDIENCE_BASIC_NAME}' → '{TestData.AUDIENCE_EDITED_NAME}'",
                name="Изменение названия",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3.5. Нажать кнопку 'Сохранить'"):
            audiences_page.form.save()
            audiences_page.form.wait_for_hidden()

            allure.attach(
                "Изменения сохранены, форма закрыта",
                name="Сохранение изменений",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3.6. Проверить изменение названия в таблице"):
            # Ищем по НОВОМУ названию
            audiences_page.search.search(TestData.AUDIENCE_EDITED_NAME)
            audiences_page.page.wait_for_timeout(1000)

            row_count = audiences_page.table.row_count
            assert row_count == 1, f"Ожидалась 1 запись по новому названию, найдено {row_count}"
            assert audiences_page.is_audience_present(TestData.AUDIENCE_EDITED_NAME, timeout=2000), \
                f"Аудитория с новым названием '{TestData.AUDIENCE_EDITED_NAME}' не найдена"

            test_flags['flag_edit'] = 1

            allure.attach(
                f"Новая аудитория найдена: '{TestData.AUDIENCE_EDITED_NAME}'",
                name="Проверка нового названия",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3.7. Проверить, что старое название не находится"):
            # Ищем по СТАРОМУ названию
            audiences_page.search.search(TestData.AUDIENCE_BASIC_NAME)
            audiences_page.page.wait_for_timeout(1000)

            # ВАЖНО: Проверяем, что аудитория с СТАРЫМ названием НЕ найдена
            is_old_present = audiences_page.is_audience_present(TestData.AUDIENCE_BASIC_NAME, timeout=2000)

            # Добавляем дополнительную проверку: смотрим все строки в таблице
            all_rows = audiences_page.table.row_count
            logger.info(f"Всего строк в таблице при поиске '{TestData.AUDIENCE_BASIC_NAME}': {all_rows}")

            # Если старая аудитория всё ещё есть - это баг приложения!
            assert not is_old_present, \
                f"Старая аудитория '{TestData.AUDIENCE_BASIC_NAME}' все еще найдена после переименования! " \
                f"Возможно, приложение создало новую аудиторию вместо переименования."

            allure.attach(
                f"Старое название '{TestData.AUDIENCE_BASIC_NAME}' не найдено (строк в таблице: {all_rows})",
                name="Проверка старого названия",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Выходные данные"):
            allure.attach(
                f"flag_edit = {test_flags['flag_edit']}\n",
                name="Выходные данные алгоритма 3",
                attachment_type=allure.attachment_type.TEXT
            )

        logger.info(f"Алгоритм 3 завершен. flag_edit = {test_flags['flag_edit']}")

    # === АЛГОРИТМ 4: УДАЛЕНИЕ АУДИТОРИИ ===

    @allure.title("Алгоритм 4: Удаление аудитории (с проверкой отмены и подтверждения)")
    @allure.description("""
        Предусловия:
        - Алгоритм 3 успешно выполнен
        - Аудитория TestAudienceBasicEdited существует
        - Открыта страница "Настройки" → "Аудитории"
        
        Выходные данные:
        - flag_delete_cancel = 1/0
        - flag_delete_confirm = 1/0
        - flag_deleted = 1/0
    """)
    def test_algorithm_4_delete(self, audiences_page: AudiencesPage, test_flags):
        """Алгоритм 4: Удаление аудитории с проверкой отмены и подтверждения"""

        if test_flags['flag_edit'] != 1:
            pytest.skip("Алгоритм 3 не выполнен успешно, пропускаем алгоритм 4")

        test_flags['flag_delete_cancel'] = 0
        test_flags['flag_delete_confirm'] = 0
        test_flags['flag_deleted'] = 0

        # === ЧАСТЬ A: ПРОВЕРКА ОТМЕНЫ УДАЛЕНИЯ ===

        with allure.step("Часть A: Проверка отмены удаления"):
            with allure.step("4.1. Найти аудиторию для удаления"):
                audiences_page.search.search(TestData.AUDIENCE_EDITED_NAME)
                assert audiences_page.table.row_count == 1, "Аудитория не найдена для удаления"

                allure.attach(
                    f"Аудитория найдена: '{TestData.AUDIENCE_EDITED_NAME}'",
                    name="Поиск аудитории для удаления",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("4.2. Инициировать удаление"):
                audiences_page.initiate_delete_audience(TestData.AUDIENCE_EDITED_NAME)

                allure.attach(
                    "Удаление инициировано",
                    name="Инициация удаления",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("4.3. Проверить модальное окно"):
                audiences_page.modal.verify_delete_confirmation_modal()

                allure.attach(
                    "Модальное окно проверено",
                    name="Проверка модального окна",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("4.4. Нажать кнопку 'Отмена'"):
                audiences_page.modal.cancel()
                audiences_page.modal.wait_for_close()

                allure.attach(
                    "Кнопка 'Отмена' нажата, модальное окно закрыто",
                    name="Отмена удаления",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("4.5. Проверить что аудитория не удалена"):
                audiences_page.search.search(TestData.AUDIENCE_EDITED_NAME)

                is_present = audiences_page.is_audience_present(TestData.AUDIENCE_EDITED_NAME)
                assert is_present, "Аудитория удалена после отмены"
                assert audiences_page.table.row_count == 1, "Количество записей изменилось"

                test_flags['flag_delete_cancel'] = 1

                allure.attach(
                    f"После отмены удаления:\n"
                    f"- Аудитория присутствует: Да\n"
                    f"- Количество записей: 1\n"
                    f"- flag_delete_cancel = {test_flags['flag_delete_cancel']}",
                    name="Проверка после отмены",
                    attachment_type=allure.attachment_type.TEXT
                )

        # === ЧАСТЬ B: ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ ===

        with allure.step("Часть B: Подтверждение удаления"):
            with allure.step("4.6. Снова инициировать удаление"):
                audiences_page.initiate_delete_audience(TestData.AUDIENCE_EDITED_NAME)

                allure.attach(
                    "Повторная инициация удаления",
                    name="Инициация удаления (второй раз)",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("4.7. Нажать кнопку 'Да' для подтверждения"):
                audiences_page.modal.wait_for_open(timeout=5000)
                audiences_page.modal.confirm()
                audiences_page.modal.wait_for_close(timeout=5000)

                allure.attach(
                    "Кнопка 'Да' нажата, удаление подтверждено",
                    name="Подтверждение удаления",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("4.8. Проверить что аудитория удалена из таблицы"):
                audiences_page.search.search(TestData.AUDIENCE_EDITED_NAME)

                row_count = audiences_page.table.row_count
                assert row_count == 0, f"Аудитория все еще найдена. Количество: {row_count}"

                test_flags['flag_delete_confirm'] = 1

                allure.attach(
                    f"После подтверждения удаления:\n"
                    f"- Количество записей: 0\n"
                    f"- flag_delete_confirm = {test_flags['flag_delete_confirm']}",
                    name="Проверка после удаления",
                    attachment_type=allure.attachment_type.TEXT
                )

        # === ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ ===

        with allure.step("4.9. Проверить поиск по разным вариантам"):
            # Поиск по полному названию
            audiences_page.search.search(TestData.AUDIENCE_EDITED_NAME)
            assert audiences_page.table.row_count == 0, "Аудитория найдена по полному названию"

            # Поиск по части названия
            audiences_page.search.search("BasicEdited")
            if audiences_page.table.row_count > 0:
                assert not audiences_page.is_audience_present(TestData.AUDIENCE_EDITED_NAME), \
                    "Тестовая аудитория найдена по частичному названию"

            # Поиск по другой части
            audiences_page.search.search("Test")
            if audiences_page.table.row_count > 0:
                assert not audiences_page.is_audience_present(TestData.AUDIENCE_EDITED_NAME), \
                    "Тестовая аудитория найдена по 'Test'"

            test_flags['flag_deleted'] = 1

            allure.attach(
                "Поиск по разным вариантам выполнен:\n"
                "- Полное название: 0 результатов ✓\n"
                "- Частичное название: тестовая аудитория не найдена ✓",
                name="Проверка поиска",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("4.10. Очистить поле поиска"):
            audiences_page.search.clear_search()

            allure.attach(
                "Поле поиска очищено",
                name="Очистка поиска",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Выходные данные"):
            allure.attach(
                f"flag_delete_cancel = {test_flags['flag_delete_cancel']}\n"  
                f"flag_delete_confirm = {test_flags['flag_delete_confirm']}\n"
                f"flag_deleted = {test_flags['flag_deleted']}\n",
                name="Выходные данные алгоритма 4",
                attachment_type=allure.attachment_type.TEXT
            )

        logger.info(f"Алгоритм 4 завершен. "
                    f"flag_delete_cancel = {test_flags['flag_delete_cancel']}, " 
                    f"flag_delete_confirm = {test_flags['flag_delete_confirm']}, "
                    f"flag_deleted = {test_flags['flag_deleted']}")

    # === ИТОГОВЫЙ ОТЧЕТ ===

    @allure.step("Итоговые критерии успеха теста AUD-CRUD-001")
    def test_final_report(self, test_flags):  # ← добавить test_flags
        """Итоговый отчет по всем алгоритмам"""

        success_criteria = all([
            test_flags['flag_clean'] is not None,  # ← заменить
            test_flags['flag_create'] == 1,
            test_flags['flag_edit'] == 1,
            test_flags['flag_delete_cancel'] == 1,
            test_flags['flag_delete_confirm'] == 1,
            test_flags['flag_deleted'] == 1
        ])

        allure.attach(
            f"ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТА AUD-CRUD-001\n\n"
            f"Алгоритм 1 (Очистка): flag_clean = {test_flags['flag_clean']}\n"
            f"Алгоритм 2 (Создание): flag_create = {test_flags['flag_create']}\n"
            f"Алгоритм 3 (Редактирование): flag_edit = {test_flags['flag_edit']}\n"
            f"Алгоритм 4 (Удаление):\n"
            f"  - flag_delete_cancel = {test_flags['flag_delete_cancel']}\n"
            f"  - flag_delete_confirm = {test_flags['flag_delete_confirm']}\n"
            f"  - flag_deleted = {test_flags['flag_deleted']}\n\n"
            f"ОБЩИЙ РЕЗУЛЬТАТ: {'УСПЕШНО' if success_criteria else 'НЕУДАЧА'}",
            name="Итоговый отчет AUD-CRUD-001",
            attachment_type=allure.attachment_type.TEXT
        )

        # Проверка всех критериев успеха
        assert test_flags['flag_clean'] is not None, "Алгоритм 1 не выполнен"
        assert test_flags['flag_create'] == 1, "Алгоритм 2 не выполнен успешно"
        assert test_flags['flag_edit'] == 1, "Алгоритм 3 не выполнен успешно"
        assert test_flags['flag_delete_cancel'] == 1, "Алгоритм 4 (отмена) не выполнен успешно"
        assert test_flags['flag_delete_confirm'] == 1, "Алгоритм 4 (подтверждение) не выполнен успешно"
        assert test_flags['flag_deleted'] == 1, "Алгоритм 4 (финальная проверка) не выполнен успешно"

        logger.info("Все алгоритмы AUD-CRUD-001 выполнены успешно!")