from django.urls import path
from useraccount.views import UserLoginView, SignupView, user_profile, user_profile_edit
from django.contrib.auth.views import LogoutView

app_name = "user"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", SignupView.as_view(), name="register"),
    path("profile/<user>/userid=<int:id>/", user_profile, name="userprofile"),
    path("profile-edit/<int:id>", user_profile_edit, name="edit_profile"),
]
