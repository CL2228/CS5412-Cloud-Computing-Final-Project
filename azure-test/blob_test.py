import io
import os, uuid

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=cs5412finalproject;AccountKey=BCKE/Fy88RbuRUs5ol6BMMGa5D6pcSG1+Ly2lXJS4JIbmivT1rc7Ok7hBYfcNIZ78kPiRk+hO2HG+ASt9o9mhQ==;EndpointSuffix=core.windows.net"

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

        # contaienr_client = blob_service_client.create_container(container)
        blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
        blob_client.upload_blob(data)

    except Exception as ex:
        print("Exception:")
        print(ex)


if __name__ == "__main__":
    img_file = open("./sample.jpg", "rb")
    write_a_blob("test-container", "test-img", img_file)