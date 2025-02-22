#users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'  # Registering the 'users' namespace

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('profile/<int:user_id>/', views.profile, name='profile'),

    # Authentication URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

