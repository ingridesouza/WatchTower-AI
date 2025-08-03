from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AreaViewSet,
    CameraViewSet,
    DetectionEventViewSet,
    EventIngestView,
    HealthView,
    PpeClassViewSet,
    SiteViewSet,
)

router = DefaultRouter()
router.register(r"sites", SiteViewSet)
router.register(r"areas", AreaViewSet)
router.register(r"cameras", CameraViewSet)
router.register(r"ppe-classes", PpeClassViewSet)
router.register(r"events", DetectionEventViewSet, basename="events")

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
    path("", include(router.urls)),
    path("events/ingest", EventIngestView.as_view(), name="events-ingest"),
]
