from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def save_evidence_jpg(img_bytes: bytes, prefix: str = "events"):
    key = f"{prefix}/{uuid4().hex}.jpg"
    default_storage.save(key, ContentFile(img_bytes))
    return default_storage.url(key)
