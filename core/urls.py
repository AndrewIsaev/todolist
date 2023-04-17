from django.contrib import admin
from django.urls import path, include

from core.views import SingUpView, LoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', SingUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),
]
