from google.cloud import storage
from google.oauth2 import service_account
from config import settings

def authenticate():
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
    blob = authenticate()
    # Upload the file
    blob.upload_from_filename(settings["UPLOAD_FILE_PATH"])

def download_model():
    blob = authenticate()
    # Download to file
    blob.download_to_filename(settings["DOWNLOAD_FILE_PATH"])
