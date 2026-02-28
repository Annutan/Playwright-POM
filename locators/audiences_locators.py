"""Локаторы для страницы аудиторий и формы аудитории"""

class AudiencesPageLocators:
    """Локаторы страницы аудиторий (таблица)"""
    # === ПОИСК ===
    SEARCH_INPUT = "//input[@placeholder='Поиск по аудиториям']"

    # === ТАБЛИЦА АУДИТОРИЙ ===
    TABLE_CONTAINER = "//div[contains(@class, 'AudiencesTable_')]"
    TABLE_ROWS = "//div[contains(@class, 'AudiencesTable_audiencesTable__row_')]"

    # === КНОПКИ ДЕЙСТВИЙ НА СТРАНИЦЕ ===
    ADD_BUTTON = "//button[text()='Добавить аудиторию']"


class AudienceFormLocators:
    """Локаторы формы создания/редактирования аудитории"""
    # === ПОЛЯ ВВОДА ===
    NAME_INPUT = "//input[contains(@name, 'name')]"  # Исправлено
    INDICATOR_INPUT = "//input[contains(@placeholder, 'Добавьте сущности')]"  # Исправлено

    # === КНОПКИ ДОБАВЛЕНИЯ ИНДИКАТОРОВ ===
    ADD_POSITIVE_BTN = "//button[contains(@class, 'AudienceIndicatorsInput_addButton_green_')]"
    ADD_NEGATIVE_BTN = "//button[contains(@class, 'AudienceIndicatorsInput_addButton_red_')]"

    # === ДОБАВЛЕННЫЕ ИНДИКАТОРЫ ===
    ADDED_POSITIVE_INDICATOR_TEMPLATE = "//div[contains(@class, 'item_positive')]//span[text()='{text}']"
    ADDED_NEGATIVE_INDICATOR_TEMPLATE = "//div[contains(@class, 'item_negative')]//span[text()='{text}']"

    # === КНОПКИ ФОРМЫ ===
    SAVE_BUTTON = "//button[text()='Сохранить']"
    CANCEL_BUTTON = "//button[text()='Отмена']"


class ModalLocators:
    """Локаторы модальных окон"""
    MODAL_DIALOG = "//div[contains(@class, 'Modal_Content')]"
    MODAL_BODY = "//div[contains(@class, 'message')]"
    MODAL_CONFIRM_BTN = "//button[text()='Да']"
    MODAL_CANCEL_BTN = "//button[text()='Отмена']"


class AudienceRowLocators:
    """Локаторы для строки таблицы (шаблоны)"""
    @staticmethod
    def row_by_name(name: str):
        return f"//div[contains(@class, 'AudiencesTable_audiencesTable__row_')][.//a[text()='{name}']]"

    @staticmethod
    def name_link_by_name(name: str):
        return f"//div[contains(@class, 'AudiencesTable_audiencesTable__row_')]//a[text()='{name}']"

    @staticmethod
    def delete_button_by_name(name: str):
        return f"//div[contains(@class, 'AudiencesTable_audiencesTable__row_')][.//a[text()='{name}']]//button[contains(@class, '_deleteBtn_')]"

    @staticmethod
    def status_by_name(name: str):
        return f"//div[contains(@class, 'AudiencesTable_audiencesTable__row_')][.//a[text()='{name}']]//button[@role='switch']"