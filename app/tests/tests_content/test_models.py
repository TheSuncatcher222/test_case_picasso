from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
import re

from src.content.models import File, get_upload_path

FILENAME_PATTERN: str = r'^user_[0-9]/text/plain/example(_)?([a-zA-Z0-9]+)?\.txt$'


@pytest.mark.django_db
def test_file_creation():
    user: User = User.objects.create_user(
        username='testuser',
        password='testpassword',
    )
    file = File.objects.create(
        file=SimpleUploadedFile('example.txt', b'test file content'),
        type='text/plain',
        owner=user,
    )
    assert re.match(
        pattern=FILENAME_PATTERN,
        string=file.file.name,
    ), (
        'Для File.file необходимо проверить алгоритм создания полного пути файла'
    )
    assert file.uploaded_at is not None, (
        'Для File.uploaded_at необходимо установить параметр "auto_now_add=True"'
    )
    assert file.processed is False, (
        'Для File.processed необходимо установить параметр "default=False"'
    )
    assert file.type == 'text/plain', (
        'Значение File.type не должно модифицироваться'
    )
    assert file.owner == user, (
        'Для File.owner устанавливается неверный пользователь'
    )


@pytest.mark.django_db
def test_get_upload_path():
    user = User.objects.create_user(username='testuser', password='testpassword')
    file = File.objects.create(
        file=SimpleUploadedFile('example.txt', b'test file content'),
        type='text/plain',
        owner=user
    )
    upload_path = get_upload_path(file, 'example.txt')
    assert re.match(
        pattern=FILENAME_PATTERN,
        string=upload_path,
    ), (
        'Для get_upload_path необходимо проверить алгоритм создания полного пути файла'
    )
