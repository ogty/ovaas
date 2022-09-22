from django.urls import path

from .views import signup, login, index, logout, update_token


app_name = "account"
urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("update_token/", update_token, name="update_token"),
]
