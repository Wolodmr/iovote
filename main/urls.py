# main/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact/', views.contact_view, name='contact'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
