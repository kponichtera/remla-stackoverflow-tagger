"""
Provides download and upload functionality
For interfacing with MinIO buckets
"""
from minio import Minio
from config import settings


def authenticate():
    """Authenticates to MinIO.

    Returns:
        Minio: The MinIO client object.
    """

    # Get credentials from env variables
    return Minio(
        settings["MINIO_ENDPOINT"],
        access_key=settings["MINIO_ACCESS_KEY"],
        secret_key=settings["MINIO_SECRET_KEY"],
        # Without this, certificates are required
        secure=False
    )


def upload_model():
    """Uploads a file to the MinIO bucket.
    """
    client = authenticate()
    if not client.bucket_exists(settings["BUCKET_NAME"]):
        client.make_bucket(settings["BUCKET_NAME"])
    client.fput_object(settings["BUCKET_NAME"],
                       settings["OBJECT_NAME"], settings["UPLOAD_FILE_NAME"])


def download_model():
    """Downloads a file from the MinIO bucket.
    """
    client = authenticate()
    if not client.bucket_exists(settings["BUCKET_NAME"]):
        return
    client.fget_object(settings["BUCKET_NAME"],
                       settings["OBJECT_NAME"], settings["DOWNLOAD_FILE_NAME"])
