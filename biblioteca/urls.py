from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('acervo.urls')),
    path('api/', include('acervo.api_urls')),
]
