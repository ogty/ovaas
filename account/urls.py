from django.urls import path

from .views import signup, login, index, logout


app_name = "account"
urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
