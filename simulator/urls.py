"""simulator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from user import views as user_views
from scheduler import views as scheduler_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('register/', user_views.register, name='register'),
    path('register/<str:qr_token>', user_views.registerFromProfile,
         name='register-from-profile'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='user/logout.html'), name='logout'),
    path('museum/', include('museum.urls')),
    path('password-reset/', user_views.password_reset, name='password_reset'),
    path('password-reset-confirm/<str:token>/',
         user_views.new_password, name='password_reset_confirm'),
    path('confirm-account/<str:token>/',
         user_views.confirm_account, name='confirm-account'),
    path('api/userinfo/<str:qr_token>',
         user_views.get_user_info, name='user-info'),
    path('badges/', include('badges.urls')),
    path('payments/', include('payments.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include('game.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
