import io
import os, uuid

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__, ContentSettings

CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=cs5412finalproject;AccountKey=IY/FhO+zJy+jui2TmIcHKp3uyWEZ/9eAxx/DnSsa0edvVOFIJnJrSiEKLYxUCXUBy8HRieupaXfg+AStBlMzjg==;EndpointSuffix=core.windows.net"


def read_a_blob(container, blob):
    """
    get the raw bytes from the blob storage
    :param container: container name
    :param blob: blob name
    :return: raw bytes
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)

        blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
        raw_bytes = blob_client.download_blob().readall()
        print("got")
        return raw_bytes

    except Exception as ex:
        print('Exception:')
        print(ex)
        return ex


def write_a_blob(container, blob, data):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
        # container_client = blob_service_client.create_container(container)
        # print(container_client.exists())
        # if not container_client.exists():
        #     blob_service_client.create()
        blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
        blob_client.upload_blob(data)

    except Exception as ex:
        print("Exception:")
        print(ex)


if __name__ == "__main__":
    img_file = open("./sample.jpg", "rb")
    write_a_blob("test-container", "tenants/myfolder/test-img.jpg", img_file)
    # try:
    #     blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    #     container_client = blob_service_client.get_container_client("test-container")
    #     blob_client = blob_service_client.get_blob_client("test-container", "test.jpg")
    #     # blobs = container_client.list_blobs()
    #     # blob_downloader = blob_client.download_blob()
    #     # print(blob_downloader.readall())
    #     img_setting = ContentSettings(content_type='image/jpeg')
    #     data = open("./DSC_7123.JPG", "rb")
    #     blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
    # except Exception as ex:
    #     print("Exception:")
    #     print(ex)

    # blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    # container_client = blob_service_client.get_container_client("my-container")
    # blob_client = blob_service_client.get_blob_client("test-container", "test.jpg")
    # # blobs = container_client.list_blobs()
    # print(container_client.exists())
    # if not container_client.exists():
    #     container_client.create_container()

