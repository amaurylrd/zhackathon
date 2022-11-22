from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=True)
router.register(r"festivals", views.FestivalViewSet, basename="festivals")
router.register(r"comments", views.CommentViewSet, basename="comments")
# router.register(r"fest", views.FestivalList)
# router.register(r"fest", views.FestivalDetail)
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path(".well-known/openapi.yaml", SpectacularAPIView.as_view(), name="openapi"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls), name="api"),
    # path("logout/", UserView.as_view(), name="logout"),
    # path("register/", RegisterView.as_view(), name="auth-register"),
]
