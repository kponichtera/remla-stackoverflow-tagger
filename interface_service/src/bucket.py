"""
Provides download and upload functionality
For interfacing with MinIO buckets
"""
import os
from joblib import load

from minio import Minio
from src.config import settings
from src.var_names import VarNames

from src.color_module import ColorsPrinter

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
    model_path = ColorsPrinter.get_color_string(
        settings[VarNames.MODEL_LOCAL_PATH.value],
        ColorsPrinter.OK_BLUE
    )
    bucket_name = ColorsPrinter.get_color_string(
        settings[VarNames.BUCKET_NAME.value],
        ColorsPrinter.OK_BLUE
    )
    model_name = ColorsPrinter.get_color_string(
        settings[VarNames.MODEL_OBJECT_KEY.value],
        ColorsPrinter.OK_BLUE
    )
    ColorsPrinter.log_print_info(f'Uploading model from path\
        {model_path} to bucket {bucket_name} as {model_name}')

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

    model_path = ColorsPrinter.get_color_string(
        settings[VarNames.MODEL_LOCAL_PATH.value],
        ColorsPrinter.OK_BLUE
    )
    bucket_name = ColorsPrinter.get_color_string(
        settings[VarNames.BUCKET_NAME.value],
        ColorsPrinter.OK_BLUE
    )
    model_name = ColorsPrinter.get_color_string(
        settings[VarNames.MODEL_OBJECT_KEY.value],
        ColorsPrinter.OK_BLUE
    )
    ColorsPrinter.log_print_info(f'Downloading model {model_name}\
        from bucket {bucket_name} to {model_path}')

    client = authenticate()
    if not client.bucket_exists(settings[VarNames.BUCKET_NAME.value]):
        return False
    client.fget_object(settings[VarNames.BUCKET_NAME.value],
                       settings[VarNames.MODEL_OBJECT_KEY.value],
                       settings[VarNames.MODEL_LOCAL_PATH.value])
    return True

def load_model():
    """Loads a model from the specified path.

    Returns:
        The loaded scikitlearn model.
    """
    ColorsPrinter.log_print_info('Attempting to load new model from bucket...')
    if not os.path.isfile(settings[VarNames.MODEL_LOCAL_PATH.value]):
        ColorsPrinter.log_print_fail(f'No model available at\
            {settings[VarNames.MODEL_LOCAL_PATH.value]}')
        return None
    model = load(settings[VarNames.MODEL_LOCAL_PATH.value])

    ColorsPrinter.log_print_info('Model loading succeeded')
    return model
