from django.urls import path
from .views import UsersView, LoginView, UsersDetailView

urlpatterns = [
    path("users/", UsersView.as_view()),
    path("users/login/", LoginView.as_view()),
    path("users/<int:user_id>/", UsersDetailView.as_view())
]
