from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import FestivalView

router = SimpleRouter(trailing_slash=True)
router.register(r"festivals", FestivalView, basename="festivals")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls), name="api"),
]
