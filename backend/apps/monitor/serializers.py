from rest_framework import serializers

from .models import Area, Camera, DetectionEvent, PpeClass, Site


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"


class PpeClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpeClass
        fields = "__all__"


class DetectionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionEvent
        fields = "__all__"
