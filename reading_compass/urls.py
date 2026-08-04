from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import include, path

from books.views import RegisterView, SafeLoginView


urlpatterns = [
    path("health/", lambda request: HttpResponse("ok"), name="health-check"),
    path("admin/", admin.site.urls),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        SafeLoginView.as_view(),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("books.urls")),
]
