from django.conf import settings
from rest_framework.serializers import ModelSerializer, ValidationError

from src.content.models import File, FILE_VALID_EXTS, FILE_VALID_EXT_STR
from src.content.tasks import process_file


class FileSerializer(ModelSerializer):
    """Сериализатор загрузки файлов на сервер."""

    class Meta:
        model = File
        fields = (
            'file',
            'uploaded_at',
            'processed',
            'type',
            'owner',
        )
        extra_kwargs = {
            'type': {'write_only': True},
            'owner': {'write_only': True},
        }

    def validate_type(self, value):
        if value not in FILE_VALID_EXTS:
            raise ValidationError(
                f'Формат {value} временно не поддерживается. '
                f'Пожалуйста, используйте: {FILE_VALID_EXT_STR}'
            )
        return value

    def save(self, **kwargs):
        isinstance: File = super().save(**kwargs)
        process_file.delay(
            isinstance.type,
            f'{settings.MEDIA_ROOT}/{str(isinstance.file)}',
            isinstance.id
        )
        return isinstance
