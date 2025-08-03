import io
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from apps.monitor.models import Area, Camera, Site


def auth_client():
    User = get_user_model()
    User.objects.create_user(username="tester", password="x")
    client = APIClient()
    token = client.post(
        "/api/auth/token/", {"username": "tester", "password": "x"}
    ).json()["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@patch("apps.monitor.services.inference_client.run_inference")
@patch("apps.monitor.services.storage.save_evidence_jpg")
def test_ingest_ok(mock_save, mock_inf, db):
    mock_inf.return_value = ({"detections": [{"label": "person"}], "model": "stub"}, 5)
    mock_save.return_value = "http://minio/evidences/frame.jpg"

    site = Site.objects.create(name="S1")
    area = Area.objects.create(site=site, name="A1")
    cam = Camera.objects.create(area=area, name="C1")

    client = auth_client()
    url = reverse("events-ingest")
    file = io.BytesIO(b"\xff\xd8\xff")
    file.name = "test.jpg"
    resp = client.post(url, {"camera_id": cam.id, "image": file}, format="multipart")
    assert resp.status_code == 201
    data = resp.json()
    assert data["camera"] == cam.id
