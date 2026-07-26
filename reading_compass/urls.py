from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from books.views import RegisterView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("books.urls")),
]

