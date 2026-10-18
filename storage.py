import io
from datetime import timedelta
from uuid import uuid4
from minio import Minio
from backend.config import settings

_client: Minio | None = None


def client() -> Minio:
    global _client
    if _client is None:
        _client = Minio(settings.minio_endpoint, settings.minio_access_key,
                        settings.minio_secret_key, secure=settings.minio_secure)
    return _client


def upload(bucket: str, data: bytes, ext: str = "jpg", content_type: str = "image/jpeg") -> str:
    key = f"{uuid4().hex}.{ext}"
    client().put_object(bucket, key, io.BytesIO(data), len(data), content_type=content_type)
    return f"{bucket}/{key}"


def download(object_key: str) -> bytes:
    bucket, key = object_key.split("/", 1)
    r = client().get_object(bucket, key)
    try:
        return r.read()
    finally:
        r.close()
        r.release_conn()


def presigned_url(object_key: str, minutes: int = 5) -> str:
    bucket, key = object_key.split("/", 1)
    return client().presigned_get_object(bucket, key, expires=timedelta(minutes=minutes))
