"""
Provides download and upload functionality
For interfacing with Google Cloud Storage buckets
"""

from google.cloud import storage
from google.oauth2 import service_account
from config import settings

def authenticate():
    """Authenticates to the Google Cloud environment
    Using environment variables returns the corresponding blob
    For the desired project and bucket.

    Returns:
        Blob: The blob of the corresponding file to be uploaded
    """

    # Get credentials from env variables
    credentials_dict = {
        "client_email": settings["CLIENT_EMAIL"],
        "token_uri": settings["TOKEN_URI"],
        # Backslashes are doubled in the environment
        "private_key": settings["PRIVATE_KEY"].replace('\\n', '\n')
    }

    # Build credentials object from dict
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # Build the client with the project and the credentials
    client = storage.Client(project=settings["PROJECT_NAME"], credentials=credentials)

    # Get the bucket
    mybucket = client.get_bucket(settings["BUCKET_NAME"])

    # Get the blob
    return mybucket.blob(settings["BLOB_NAME"])

def upload_model():
    """Uploads a file to the Google Cloud Storage bucket.
    """
    blob = authenticate()
    # Upload the file
    blob.upload_from_filename(settings["UPLOAD_FILE_PATH"])

def download_model():
    """Downloads a file from the Google Cloud Storage bucket.
    """
    blob = authenticate()
    # Download to file
    blob.download_to_filename(settings["DOWNLOAD_FILE_PATH"])
