#file: project/urls.py
# A projekt fő URL konfigurációja. Ide kerülnek az admin felület
# útvonalai, valamint a core alkalmazás URL-jeinek összekapcsolása.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin felület
    path('admin/', admin.site.urls),

    # Core alkalmazás URL-jei (index, API-k stb.)
    path("", include("core.urls")),
]

# Media fájlok kiszolgálása fejlesztői módban
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
