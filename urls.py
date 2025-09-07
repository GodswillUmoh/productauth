# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page shows base.html
    path('generate/', include('authentication.urls')),  # Routes for your app
]

# Serve static and media in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
