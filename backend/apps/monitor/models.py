from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Site(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True, default="")
    timezone = models.CharField(max_length=64, default="UTC")

    def __str__(self):
        return self.name


class Area(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.site.name} / {self.name}"


class Camera(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="cameras")
    name = models.CharField(max_length=120)
    rtsp_url = models.TextField(blank=True, default="")
    active = models.BooleanField(default=True)
    fps_capture = models.PositiveIntegerField(default=2)
    roi_polygon = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.area})"


class PpeClass(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class DetectionEvent(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField(db_index=True, default=timezone.now)
    has_violation = models.BooleanField(default=False)
    violation_types = ArrayField(
        models.CharField(max_length=64), default=list, blank=True
    )
    detections = models.JSONField()
    image_url = models.TextField(null=True, blank=True)
    processed_by = models.CharField(max_length=64, default="stub")
    latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["site", "timestamp_utc"]),
            models.Index(fields=["area", "timestamp_utc"]),
        ]
