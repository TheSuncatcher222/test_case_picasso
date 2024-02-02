import pytest

from tests.fixtures import (
    client_anon,
    URL_AUTH_REGISTER, URL_AUTH_TOKEN, URL_AUTH_TOKEN_REFRESH,
    URL_DOCS, URL_SWAGGER,
    URL_AVAILABLE_STATUSES,
)


@pytest.mark.django_db
class TestEndpointsAvailability():
    """
    Производит тест доступности эндпоинтов в urlpatterns.
    Тестируется именно доступность эндпоинтов, а не права доступа к ним.
    """

    @pytest.mark.parametrize(
        'url, meaning', [
            (URL_AUTH_REGISTER,
             'регистрации пользователей'
             ),
            (URL_AUTH_TOKEN,
             'получения токенов доступа и обновления'
             ),
            (URL_AUTH_TOKEN_REFRESH,
             'обновления токена доступа'
             ),
        ]
    )
    def test_auth(self, url, meaning) -> None:
        """Производит тест доступности эндпоинтов auth."""
        response = client_anon().get(url)
        assert response.status_code in URL_AVAILABLE_STATUSES, (
            f'Убедитесь, что эндпоинт {meaning} функционирует '
            f'и доступен по адресу "{url}".'
        )
        return

    @pytest.mark.parametrize(
        'url, meaning', [
            (URL_DOCS, 'схемы документации'),
            (URL_SWAGGER, 'Swagger представления'),
        ]
    )
    def test_schema(self, url, meaning) -> None:
        """Производит тест доступности эндпоинтов drf_spectacular."""
        response = client_anon().get(url)
        assert response.status_code in URL_AVAILABLE_STATUSES, (
            f'Убедитесь, что эндпоинт получения {meaning} документации '
            f'функционирует и доступен по адресу "{url}".'
        )
        return
