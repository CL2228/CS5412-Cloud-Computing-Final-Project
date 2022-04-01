from ..config import azureStorageConnectString
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings


def read_blob(container, blob):
    """
    get blob data
    :param container: container name of the blob
    :param blob: blob name
    :return: byte data of the blob
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectString)
        blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
        if not blob_client.exists():
            return False, "Blob doesn't exist"
        return True, blob_client.download_blob().readall()
    except Exception as ex:
        return False, ex


def write(container, blob, data, content_type=None):
    """
    write data to a blob
    :param container: name of container
    :param blob: name of blob
    :param data: data, in bytes format
    :param content_type: content-type of the bytes
    :return: Ture if successfully uploaded
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectString)
        container_client = blob_service_client.get_container_client(container)
        if not container_client.exists():
            container_client.create_container()
        blob_client = blob_service_client.get_blob_client(container=container, blob=blob)

        if content_type is not None:
            blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type=content_type))
        else:
            blob_client.upload_blob(data, overwrite=True)
        return True, "Uploaded successfully."
    except Exception as ex:
        return False, ex



if __name__ == "__main__":
    data_status, data = read_blob("test-container", "test.jpg")
    print(data)
