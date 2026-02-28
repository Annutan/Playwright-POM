"""Конфигурация логгера"""
import logging
import sys


def setup_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Добавляем обработчик только если его еще нет
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger