from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from src.auth.urls import urlpatterns as urlpatterns_auth

urlpatterns_api = [
    path('auth/', include(urlpatterns_auth)),
]

urlpatterns_docs = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns_api)),
    path('docs/', include(urlpatterns_docs)),
]
