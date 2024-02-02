import pytest

from tests.fixtures import (
    client_anon,
    URL_CONTENT,
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
            (URL_CONTENT, 'загрузки и получения файлов'),
        ]
    )
    def test_content(self, url, meaning) -> None:
        """Производит тест доступности эндпоинтов content."""
        response = client_anon().get(url)
        assert response.status_code in URL_AVAILABLE_STATUSES, (
            f'Убедитесь, что эндпоинт получения {meaning} документации '
            f'функционирует и доступен по адресу "{url}".'
        )
        return
