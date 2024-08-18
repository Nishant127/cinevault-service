from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="user-registration"),
    path("login/", views.LoginView.as_view(), name="user-login")
]
