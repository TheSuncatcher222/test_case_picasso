from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from src.content.models import File
from src.content.serializers import FileSerializer


# INFO: можно и FileSend(CreateAPIView) использовать. Был выбрал ModelViewSet
#       по той причине, что когда идет работа с моделями, проще сначала
#       в фреймворке создать полный функционал, а потом просто его ограничить.
#       Это не отбирает производительность, код пишется намного быстрее,
#       быстрее читается, быстрее расширяется.
#       Я бы использовал CreateAPIView, например, при ручной авторизации,
#       или при каких-то "точечных" действиях.
class FileViewSet(ModelViewSet):
    """Viewset для работы с загружаемыми файлами."""

    http_method_names = ('get', 'post',)
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = File.objects.all()

    def create(self, request, *args, **kwargs):
        uploaded_file: InMemoryUploadedFile = self.request.FILES.get('file')
        request.data['type']: str = uploaded_file.content_type
        request.data['owner']: User = self.request.user.id
        return super().create(request, *args, **kwargs)
