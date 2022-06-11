"""
Provides download and upload functionality
For interfacing with MinIO buckets
"""
from minio import Minio
from interface_service.config import settings
from interface_service.var_names import VarNames


def authenticate():
    """Authenticates to the object storage environment.

    Returns:
        Minio: The MinIO client object.
    """

    # Get credentials from env variables
    return Minio(
        settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
        access_key=settings[VarNames.OBJECT_STORAGE_ACCESS_KEY.value],
        secret_key=settings[VarNames.OBJECT_STORAGE_SECRET_KEY.value],
        # Without this, certificates are required
        secure=settings[VarNames.OBJECT_STORAGE_TLS.value]
    )


def upload_model():
    """Uploads a file to the object storage bucket.
    """
    client = authenticate()
    if not client.bucket_exists(settings[VarNames.BUCKET_NAME.value]):
        client.make_bucket(settings[VarNames.BUCKET_NAME.value])
    client.fput_object(settings[VarNames.BUCKET_NAME.value],
                       settings[VarNames.MODEL_OBJECT_KEY.value],
                       settings[VarNames.MODEL_LOCAL_PATH.value])


def download_model():
    """Downloads a file from the object storage bucket.

    Returns:
        bool: Whether the download was successful.
    """
    client = authenticate()
    if not client.bucket_exists(settings[VarNames.BUCKET_NAME.value]):
        return False
    client.fget_object(settings[VarNames.BUCKET_NAME.value],
                       settings[VarNames.MODEL_OBJECT_KEY.value],
                       settings[VarNames.MODEL_LOCAL_PATH.value])
    return True
