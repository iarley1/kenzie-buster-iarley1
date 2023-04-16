from django.urls import path
from .views import UsersView, LoginView

urlpatterns = [
    path("users/", UsersView.as_view()),
    path("users/login/", LoginView.as_view())
]
