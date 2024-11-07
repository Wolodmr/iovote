from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import contact_view


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact/', contact_view, name='contact'),    
    # path('static/<path:path>/', serve_static_files),  # Adjust if necessary
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
