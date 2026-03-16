from django.urls import path
from . import views
from .auth_views import login_view, logout_view

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
