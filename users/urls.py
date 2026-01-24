from django.urls import path
from .views import LoginView, ProfileView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login")
]