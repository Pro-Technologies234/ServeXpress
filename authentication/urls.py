from django.urls import path
from .views import register, logout_view, log_in, set_new_password, password_reset, change_password, user_profile

urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", log_in, name="log_in"),
    path("password_reset/", password_reset, name="password_reset" ),
    path("set_new_password/<str:uidb64>/<str:token>/", set_new_password, name="set_new_password" ),
    path("change_password/", change_password, name="change_password" ),
    path("account/profile/", user_profile, name="user_profile" ),
]