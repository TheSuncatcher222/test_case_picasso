from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.content.views import FileViewSet

router: DefaultRouter = DefaultRouter()

router.register(prefix='', viewset=FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
