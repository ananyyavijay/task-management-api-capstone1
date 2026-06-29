from azure.storage.blob import BlobServiceClient
from app.config import settings

blob_service = BlobServiceClient.from_connection_string(
    settings.AZURE_STORAGE_CONNECTION_STRING
)

container_client = blob_service.get_container_client(
    settings.BLOB_CONTAINER_NAME
)

try:
    container_client.create_container()
except Exception:
    # Container already exists
    pass