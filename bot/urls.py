from django.urls import path

from bot.views import VerifyUserView

urlpatterns = [
    path('verify', VerifyUserView.as_view(), name='verify_bot'),
]
