from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='generate/')),  # 👈 Add this line
    path('generate/', views.generate_code, name='generate_code'),
    path('verify/<uuid:code>/', views.verify_code, name='verify_code'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-zip/', views.download_all_codes, name='download_all_codes'), 
    path("download/pdf/", views.download_all_codes_pdf, name="download_all_codes_pdf"),
    path("download/zip/", views.download_all_codes_zip, name="download_all_codes_zip"),  
    
    
]

