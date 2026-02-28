"""Настройка логгера"""
import logging
import os


def setup_logger():
    """Настройка логгера"""
    # Создаем логгер
    logger = logging.getLogger("autotests")

    # Если логгер уже настроен, возвращаем его
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Консольный хендлер
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)-8s | %(message)s'))

    # Добавляем хендлеры
    logger.addHandler(console_handler)

    return logger


# Глобальный логгер
logger = setup_logger()