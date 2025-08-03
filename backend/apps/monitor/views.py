from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import EventFilter
from .models import Area, Camera, DetectionEvent, PpeClass, Site
from .serializers import (
    AreaSerializer,
    CameraSerializer,
    DetectionEventSerializer,
    PpeClassSerializer,
    SiteSerializer,
)
from .services.inference_client import run_inference
from .services.rules import evaluate_violation
from .services.storage import save_evidence_jpg


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]


class PpeClassViewSet(viewsets.ModelViewSet):
    queryset = PpeClass.objects.all()
    serializer_class = PpeClassSerializer
    permission_classes = [IsAuthenticated]


class DetectionEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetectionEvent.objects.all().order_by("-timestamp_utc")
    serializer_class = DetectionEventSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EventFilter


class EventIngestView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = []

    async def post(self, request):
        camera_id = request.POST.get("camera_id")
        image = request.FILES.get("image")
        if not camera_id or not image:
            return Response(
                {"detail": "camera_id e image são obrigatórios"}, status=400
            )

        camera = get_object_or_404(Camera, pk=camera_id)
        area = camera.area
        site = area.site

        file_bytes = image.read()
        inf, latency_ms = await run_inference(file_bytes, filename=image.name)
        detections = inf.get("detections", [])
        processed_by = inf.get("model", "unknown")

        image_url = save_evidence_jpg(file_bytes)

        has_violation, violation_types = evaluate_violation(detections)

        event = DetectionEvent.objects.create(
            site=site,
            area=area,
            camera=camera,
            has_violation=has_violation,
            violation_types=violation_types,
            detections=detections,
            image_url=image_url,
            processed_by=processed_by,
            latency_ms=latency_ms,
        )

        return Response(
            DetectionEventSerializer(event).data, status=status.HTTP_201_CREATED
        )
