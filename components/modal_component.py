"""
Компонент модального окна
Использует ModalElement и ButtonElement из папки elements
"""
import allure
from playwright.sync_api import Page, Locator
from ..elements.modal_element import ModalElement
from ..elements.button_element import ButtonElement
from ..elements.text_element import TextElement
from .base_component import BaseComponent
from ..locators.audiences_locators import ModalLocators
import logging

logger = logging.getLogger(__name__)


class ModalComponent(BaseComponent):
    """Компонент модального окна с паттерном подтверждения/отмены"""

    def __init__(self, page: Page, root_locator: Locator, name: str = "модальное окно"):
        super().__init__(page, root_locator, name)

        # Используем ModalElement из папки elements
        self.modal = ModalElement(
            root_locator.first,  # Берем первый, если их несколько
            name=f"{self.name} - базовый элемент"
        )

        # Используем ButtonElement для кнопок
        self.confirm_button = ButtonElement(
            self._locator(ModalLocators.MODAL_CONFIRM_BTN).first,
            name=f"{self.name} - кнопка подтверждения"
        )

        self.cancel_button = ButtonElement(
            self._locator(ModalLocators.MODAL_CANCEL_BTN).first,
            name=f"{self.name} - кнопка отмены"
        )

        # Используем TextElement для тела модального окна
        self.body_text = TextElement(
            self._locator(ModalLocators.MODAL_BODY).first,
            name=f"{self.name} - текст"
        )

    @allure.step("Проверить модальное окно подтверждения удаления")
    def verify_delete_confirmation_modal(self, expected_text: str = None) -> 'ModalComponent':
        """
        Проверка модального окна подтверждения удаления
        :param expected_text: ожидаемый текст подтверждения (если None, используется стандартный)
        """
        logger.info(f"Проверяю модальное окно подтверждения удаления")

        # 1. Проверяем что модальное окно открылось
        assert self.modal.wait_for_open(timeout=5000), "Модальное окно не отображается"

        # 2. Проверяем текст подтверждения
        if expected_text is None:
            expected_text = "Вы уверены, что хотите безвозвратно удалить аудиторию?"

        actual_text = self.body_text.get_text()
        assert expected_text in actual_text, \
               f"Неверный текст в модальном окне.\nОжидалось: {expected_text}\nПолучено: {actual_text}"

        # 3. Проверяем наличие кнопок
        assert self.confirm_button.is_visible(), "Кнопка 'Да' не найдена"
        assert self.cancel_button.is_visible(), "Кнопка 'Отмена' не найдена"

        logger.info("Модальное окно подтверждения удаления проверено успешно")
        return self

    @allure.step("Проверить модальное окно (общая проверка)")
    def verify_modal(self, expected_text: str = None) -> 'ModalComponent':
        """
        Общая проверка модального окна
        :param expected_text: ожидаемый текст (если None, проверяется только наличие)
        """
        assert self.modal.wait_for_open(timeout=5000), "Модальное окно не отображается"

        if expected_text:
            actual_text = self.body_text.get_text()
            assert expected_text in actual_text, \
                   f"Неверный текст в модальном окне.\nОжидалось: {expected_text}\nПолучено: {actual_text}"

        return self

    @allure.step("Подтвердить действие в модальном окне")
    def confirm(self) -> 'ModalComponent':
        """Подтверждение действия (нажать 'Да')"""
        logger.info(f"Подтверждаю действие в {self.name}")

        self.confirm_button.wait_for_visible(timeout=5000)
        self.confirm_button.click()
        logger.info("Кнопка подтверждения нажата")

        # Ждем закрытия
        self.modal.wait_for_close(timeout=5000)

        return self

    @allure.step("Отменить действие в модальном окне")
    def cancel(self) -> 'ModalComponent':
        """Отмена действия (нажать 'Отмена')"""
        logger.info(f"Отменяю действие в {self.name}")

        self.cancel_button.wait_for_visible(timeout=5000)
        self.cancel_button.click()
        logger.info("Кнопка отмены нажата")

        self.modal.wait_for_close(timeout=5000)

        return self

    @allure.step("Получить текст модального окна")
    def get_text(self) -> str:
        """Получение текста модального окна"""
        return self.body_text.get_text()

    def wait_for_open(self, timeout: int = 5000) -> bool:
        """Ожидание открытия модального окна"""
        try:
            self.modal.wait_for_open(timeout)
            return True
        except Exception:
            return False

    def wait_for_close(self, timeout: int = 5000) -> bool:
        """Ожидание закрытия модального окна"""
        try:
            self.modal.wait_for_close(timeout)
            return True
        except Exception:
            return False

    @property
    def is_open(self) -> bool:
        """Проверка, открыто ли модальное окно"""
        return self.modal.is_visible(timeout=1000)