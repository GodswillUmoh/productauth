'''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Root URL
    #path('', include('authentication.urls')),
    path('generate/', include('authentication.urls')),
    #path('auth/', include('authentication.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

# project/urls.py

# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page shows base.html
    path('generate/', include('authentication.urls')),  # All app pages under /auth/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




