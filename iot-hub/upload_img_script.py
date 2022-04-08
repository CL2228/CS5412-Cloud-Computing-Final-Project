import asyncio
import os
from azure.iot.device.aio import IoTHubDeviceClient
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobClient
from functions.server_functions.blob.azure_blob_helpers import generate_file_name, check_img_file_suffix
import event_hub_helper


DEVICE_CONN_STR = "HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=test-device;SharedAccessKey=Fj13ZONv0svBqCmqk7BG29Aqd1tF/7P5983RJLbF6zk="
PATH_OF_FILE = "./sample.jpg"


async def upload_img_from_device(connection_string: str, file_path: str):
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    try:
        await device_client.connect()
        blob_name = os.path.basename(file_path)
        storage_info = await device_client.get_storage_info_for_blob(blob_name)
        print(storage_info)

        check_img, suffix = check_img_file_suffix(PATH_OF_FILE)
        if not check_img:
            return False, "Not an image"

        img_name = generate_file_name(prefix="")


    except FileNotFoundError:
        return False, "File Not Found."
    except Exception as ex:
        return False, ex
    finally:
        await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(upload_img_from_device(DEVICE_CONN_STR, PATH_OF_FILE))