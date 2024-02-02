import os

from src.settings import BASE_DIR, DATABASES


class TestProdSettings():
    """Производит тест настроек проекта перед деплоем на сервер."""

    def test_db_is_postgresql(self) -> None:
        """Проверяет, что база данных проекта: PostgreSQL."""
        assert DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql', (
            'Установите для settings.DATABASES '
            'значение "django.db.backends.postgresql".'
        )
        return

    def test_env(self) -> None:
        """
        Проверяет, что в проекте существует .env файл,
        который содержит все необходимые поля.
        """
        env_file_path = os.path.join(BASE_DIR, '.env')
        assert os.path.isfile(env_file_path), 'Создайте .env файл.'
        missed_fields: list[str] = []
        ENV_DATA: dict[str, any] = {
            'SECRET_KEY': os.getenv('SECRET_KEY'),
            'DB_HOST': os.getenv('DB_HOST'),
            'DB_PORT': os.getenv('DB_PORT'),
            'POSTGRES_DB': os.getenv('POSTGRES_DB'),
            'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        }
        for key, value in ENV_DATA.items():
            if value is None:
                missed_fields.append(key)
        assert not missed_fields, (
            'В .env файле отсутствуют следующие поля: '
            f'{", ".join(field for field in missed_fields)}'
        )
        return
