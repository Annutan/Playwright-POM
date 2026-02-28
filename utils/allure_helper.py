"""Утилиты для работы с Allure"""
import allure
import json


def attach_json(data: dict, name: str = "JSON данные"):
    """Прикрепление JSON данных к отчету Allure"""
    allure.attach(
        json.dumps(data, indent=2, ensure_ascii=False),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


def attach_text(text: str, name: str = "Текстовые данные"):
    """Прикрепление текстовых данных к отчету Allure"""
    allure.attach(
        text,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )


def attach_screenshot(page, name: str = "Скриншот"):
    """Прикрепление скриншота к отчету Allure"""
    screenshot = page.screenshot()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )