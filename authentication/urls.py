'''from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'authentication'

urlpatterns = [
    #path('', RedirectView.as_view(url='generate/')),  # 👈 Add this line
    path('generate/', views.generate_code, name='generate_code'),
    path('verify/<uuid:code>/', views.verify_code, name='verify_code'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-zip/', views.download_all_codes, name='download_all_codes'), 
    path("download/pdf/", views.download_all_codes_pdf, name="download_all_codes_pdf"),
    path("download/zip/", views.download_all_codes_zip, name="download_all_codes_zip"),  
    path('scan/', views.scan_qr_page, name='scan_qr'),
    #path('verify/<str:code>/', views.verify_product, name='verify_product'),

]
'''

# authentication/urls.py
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_code, name='generate_code'),
    path('verify/<uuid:code>/', views.verify_code, name='verify_code'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-zip/', views.download_all_codes, name='download_all_codes'), 
    path('download/pdf/', views.download_all_codes_pdf, name='download_all_codes_pdf'),
    path('download/zip/', views.download_all_codes_zip, name='download_all_codes_zip'),  
    path('scan/', views.scan_qr_page, name='scan_qr'),
    path("download/pdf/", views.download_all_codes_pdf, name="download_all_codes_pdf"),
    
]



   

