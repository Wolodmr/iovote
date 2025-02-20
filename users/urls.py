#users/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import signup, CustomLogoutView



app_name = 'users'  # This registers the 'users' namespace

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('signup/', views.signup, name='signup'),
    # path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

