from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
import pytest

from src.content.models import File
from tests.fixtures import (  # noqa (F401)
    client_auth, client_auth_admin, create_two_media,
    FILE_GIF, URL_CONTENT,
)


@pytest.mark.django_db
class TestEndpoints():
    """
    Производит тест функционала эндпоинтов в urlpatterns.
    """

    def test_content_get(self, create_two_media):  # noqa (F811)
        """Отправляет GET запрос на получение списка файлов."""
        content_count_init: int = File.objects.all().count()
        assert content_count_init == 2, (
            'Убедитесь, что в test_content_get используется фикстура, '
            'которая создает 2 объекта File, и не используются другие фикстуры.'
        )

        response = client_auth().get(path=URL_CONTENT)

        assert response.status_code == 200, (
            f'Убедитесь, что {URL_CONTENT} возвращает статус 200 при GET запросе '
            'авторизированному и не авторизированному клиенту.'
        )
        assert len(response.data) == 2, (
            f'Убедитесь, что {URL_CONTENT} возвращает все объекты Files '
            'без использования пагинации'
        )
        for file in response.data:
            assert list(file.keys()) == ['file', 'uploaded_at', 'processed'], (
                f'Убедитесь, что {URL_CONTENT} возвращает все объекты Files '
                'в формате {"file": str, "uploaded_at": str, "processed": bool}'
            )

        return

    def test_content_post(self, create_two_media):  # noqa (F811)
        """Отправляет POST запрос на получение списка файлов."""
        content_count_init: int = File.objects.all().count()
        assert content_count_init == 2, (
            'Убедитесь, что в test_content_get используется фикстура, '
            'которая создает 2 объекта File, и не используются другие фикстуры.'
        )

        gif_file: SimpleUploadedFile = SimpleUploadedFile(
            'example.gif',
            FILE_GIF,
            content_type='image/gif',
        )
        data: dict[str, any] = {'file': gif_file}
        response = client_auth_admin().post(
            path=URL_CONTENT,
            data=data,
            format='multipart',
        )

        assert response.status_code == 201, (
            f'Убедитесь, что {URL_CONTENT} возвращает статус 200 при отправке '
            'валидного POST запроса на загрузку файла.'
        )

        all_files: QuerySet = File.objects.all()
        assert all_files.count() == 3, (
            f'Убедитесь, что {URL_CONTENT} создает объект в базе данных '
            'при отправке валидного POST запроса на загрузку файла.'
        )

        # INFO: сортировка по -id
        latest_file: File = all_files.first()
        assert latest_file.processed is False, (
            f'Убедитесь, что {URL_CONTENT} создает объект в базе данных '
            'при отправке валидного POST запроса на загрузку файла.'
        )

        return
