from django.db import models
from django.contrib.auth.models import User

FILE_VALID_EXTS: list[str] = [
    # Text data
    'text/plain',
    'text/csv',
    # Image data
    'image/gif',
    'image/jpeg',
    'image/png',
]
FILE_VALID_EXT_STR: str = ', '.join(FILE_VALID_EXTS)


def get_upload_path(instance, filename):
    """
    Изменяет путь сохранения файла в зависимости от:
        - пользователя;
        - типа фала;
        - даты загрузки.
    """
    return f'user_{instance.owner.id}/{instance.type}/{filename}'


class File(models.Model):
    """Модель загружаемых файлов."""

    file = models.FileField(
        verbose_name='файл',
        upload_to=get_upload_path
    )
    uploaded_at = models.DateTimeField(
        verbose_name='дата и время загрузки',
        auto_now_add=True,
    )
    processed = models.BooleanField(
        verbose_name='статус обработанного',
        default=False,
    )
    # INFO: добавил следующие поля для лучшего контроля
    #       и структуризации процесса загрузки файлов.
    type = models.CharField(
        verbose_name='тип',
    )
    owner = models.ForeignKey(
        verbose_name='владелец',
        to=User,
        related_name='file',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return f'Файл №{self.id}: {self.type} (обработан: {self.processed})'
