from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import FestivalView

router = SimpleRouter(trailing_slash=False)
router.register(r"festival", FestivalView, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls), name="api"),
]
