"""Локаторы навигации и тулбара"""


class NavigationLocators:
    """Локаторы для навигации между разделами"""

    # Главный тулбар (верхнее меню)
    TOOLBAR_SETTINGS = "//div[contains(@class, 'Header_Navigation')]//span[text()='Настройки']"

    # Подменю раздела "Настройки" (появляется после клика)
    SUBMENU_THEMATICS = "//button[text()='Тематики']"
    SUBMENU_CHANNELS = "//button[text()='Каналы']"
    SUBMENU_AUDIENCES = "//button[text()='Аудитории']"