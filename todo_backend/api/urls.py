from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    TodoViewSet,
    register,
    login_view,
    logout_view,
    me,
)

router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")

urlpatterns = [
    path("health/", health, name="Health"),
    path("auth/register/", register, name="auth-register"),
    path("auth/login/", login_view, name="auth-login"),
    path("auth/logout/", logout_view, name="auth-logout"),
    path("auth/me/", me, name="auth-me"),
    path("", include(router.urls)),
]
