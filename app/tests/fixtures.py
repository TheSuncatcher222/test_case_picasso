from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from src.content.models import File

"""Clients."""


def client_anon() -> APIClient:
    """Возвращает объект анонимного клиента."""
    return APIClient()


def client_auth() -> APIClient:
    """
    Возвращает объект авторизированного клиента.
    Авторизация производится форсированная: без использования токенов.
    """
    auth_client = APIClient()
    auth_client.force_authenticate(user=None)
    return auth_client


def create_user_obj(num: int) -> User:
    """
    Создает и возвращает объект модели "User".
    Высокое быстродействие за счет отсутствия шифрования пароля.
    Тесты, которые требуют валидации поля "password" будут провалены!
    """
    return User.objects.create(
        username=f'test_user_{num}',
        password=f'test_user_password_{num}!PASS',
    )


def create_admin_user_obj(username, password):
    """Создает и возвращает объект администратора модели "User"."""
    admin: User = User.objects.create_superuser(
        username=username,
        password=password,
    )
    return admin


def client_auth_admin(num: int = 1, admin: User = None) -> APIClient:
    """
    Возвращает объект авторизированного клиента по JWT токену.
    """
    if admin is None:
        admin: User = create_admin_user_obj(
            username=f'admin_{num}',
            password='admin'
        )
    client: APIClient = client_anon()
    refresh: str = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


"""Fixtures."""


FILE_GIF: bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
FILE_TEXT: str = 'File with text'


@pytest.fixture()
def create_two_media() -> None:
    """
     Фикстура для наполнения БД двумя объектами File:
        - изображение gif
        - текст txt
    """
    user: User = User.objects.create_user(
        username='test_user_creator',
        password='test_password_creator',
    )
    files: list[File] = [
        File(
            file=ContentFile(FILE_GIF),
            type='image/gif',
            owner=user,
        ),
        File(
            file=ContentFile(FILE_TEXT.encode('utf-8')),
            type='text/plain',
            owner=user,
        ),
    ]
    File.objects.bulk_create(files)
    return


"""URLs."""


URL_API: str = '/api/'

URL_AUTH: str = f'{URL_API}auth/'
URL_AUTH_REGISTER: str = f'{URL_AUTH}users/'
URL_AUTH_TOKEN: str = f'{URL_AUTH}token/'
URL_AUTH_TOKEN_REFRESH: str = f'{URL_AUTH_TOKEN}refresh/'

URL_CONTENT: str = f'{URL_API}content/'

URL_DOCS: str = '/docs/'
URL_SWAGGER: str = f'{URL_DOCS}swagger/'

# INFO: статусы ответов, когда URL существует и доступен для HTTP обращений.
URL_AVAILABLE_STATUSES: list[int] = [
    status.HTTP_200_OK,
    status.HTTP_401_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN,
    status.HTTP_405_METHOD_NOT_ALLOWED,
]
