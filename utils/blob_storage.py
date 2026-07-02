import os
from uuid import uuid4

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

if not CONTAINER_NAME:
    raise RuntimeError("BLOB_CONTAINER_NAME is not configured.")


def get_blob_service_client():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if not connection_string:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING not configured")

    return BlobServiceClient.from_connection_string(connection_string)


def create_container_if_not_exists():

    blob_service = get_blob_service_client()

    container_client = blob_service.get_container_client(CONTAINER_NAME)

    try:
        container_client.create_container()
    except Exception:
        # Container already exists
        pass


def upload_file(task_id: str, filename: str, content: bytes) -> dict:

    blob_service = get_blob_service_client()

    container_client = blob_service.get_container_client(CONTAINER_NAME)

    blob_name = f"{task_id}/{uuid4()}_{filename}"

    blob_client = blob_service.get_blob_client(
        container=CONTAINER_NAME,
        blob=blob_name
    )

    blob_client.upload_blob(
        content,
        overwrite=True
    )

    return {
        "blob_name": blob_name,
        "blob_url": blob_client.url,
    }


def get_blob_url(task_id: str, filename: str) -> str:
    """
    Returns the URL of a blob without uploading it.
    """

    blob_service = get_blob_service_client()

    blob_name = f"{task_id}/{filename}"

    blob_client = blob_service.get_blob_client(
        container=CONTAINER_NAME,
        blob=blob_name
    )

    return blob_client.url