"""Тестовые данные для тестов аудиторий"""


class TestData:
    """Тестовые данные"""

    # Базовые данные из документации AUD-CRUD-001
    BASE_URL = "https://assist24.tech/app"

    # AUD-CRUD-001 данные
    AUDIENCE_BASIC_NAME = "TestAudienceBasic"
    AUDIENCE_EDITED_NAME = "TestAudienceBasicEdited"
    REQUIRED_INDICATOR = "ОБЯЗИНДИКАТОР"

    @staticmethod
    def get_unique_audience_name(prefix: str = "TestAudience"):
        """Генерация уникального имени аудитории"""
        import random
        import time
        timestamp = int(time.time())
        random_num = random.randint(100, 999)
        return f"{prefix}_{timestamp}_{random_num}"