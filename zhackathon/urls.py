from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=True)
router.register(r"festivals", views.FestivalViewSet, basename="festivals")
router.register(r"comments", views.CommentViewSet, basename="comments")
router.register(r"ratings", views.RatingViewSet, basename="ratings")
router.register(r"user", views.UserViewSet, basename="user")

urlpatterns = [
    path(".well-known/openapi.yaml", SpectacularAPIView.as_view(), name="openapi"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls), name="api"),
    # path("logout/", UserView.as_view(), name="logout"),
    # path("register/", RegisterView.as_view(), name="auth-register"),
]
