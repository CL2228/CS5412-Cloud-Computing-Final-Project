from ..config import azureStorageConnectString, blobDefaultContainer
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings


def read_blob(blob_name:str, container_name: str = blobDefaultContainer):
    """
        get blob data
    :param blob_name: the blob name
    :param container_name: the container name
    :return: [T / F, byte data of that blob / error message]
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectString)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        if not blob_client.exists():
            return False, "Blob doesn't exist"
        return True, blob_client.download_blob().readall()
    except Exception as ex:
        return False, ex


def write_blob(blob_name: str, data, container_name: str = blobDefaultContainer, content_type: str=None):
    """
        write data to a blob

    :param blob_name: name of blob
    :param data: data, in bytes (normally)
    :param container_name: name of Blob container
    :param content_type: content type : [might be an image]
    :return: [T / F, message]
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectString)
        container_client = blob_service_client.get_container_client(container)
        if not container_client.exists():
            container_client.create_container()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        if content_type is not None:
            blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type=content_type))
        else:
            blob_client.upload_blob(data, overwrite=True)
        return True, "Uploaded successfully."
    except Exception as ex:
        return False, ex


def delete_blob(blob_name: str, container_name: str = blobDefaultContainer):
    """
        delete a blob
    :param blob_name: blob's name
    :param container_name: the name of container
    :return: [T / F, message]
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectString)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        if not blob_client.exists():
            return False, "Blob doesn't exist"
        return True, "Successfully deleted that blob"
    except Exception as ex:
        return False, ex









if __name__ == "__main__":
    # data_status, data = read_blob("test-container", "test.jpg")
    # print(data)
    print("hi")
