from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from src.authentication.urls import urlpatterns as urlpatterns_auth
from src.content.urls import urlpatterns as urlpatterns_content


urlpatterns_api = [
    path('auth/', include(urlpatterns_auth)),
    path('content/', include(urlpatterns_content)),
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
