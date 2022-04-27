import asyncio
import os
from azure.iot.device.aio import IoTHubDeviceClient
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobClient
from functions.server_functions.blob import azure_blob_helpers
from functions.server_functions.mongodb import mongodb_utils
from azure.storage.blob import ContentSettings
import event_hub_helper


DEVICE_CONN_STR = "HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=gates-hall-g01;SharedAccessKey=ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="

PATH_OF_FILE = "./sample.jpg"

DEVICE_KEY = "ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="


async def upload_img_from_device(connection_string: str, device_key: str, file_path: str):
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    try:
        await device_client.connect()

        # check image format and get suffix
        check_img, suffix = azure_blob_helpers.check_img_file_suffix(file_path)
        if not check_img:
            return False, "Not an image"
        # get the unit ID and generate unique file name
        blob_name = azure_blob_helpers.generate_file_name(prefix="records/", suffix="." + suffix)

        print("reach here: {}".format(blob_name))

        storage_info = await device_client.get_storage_info_for_blob(blob_name)
        print(storage_info['blobName'])

        sas_url = "https://{}/{}/{}{}".format(
            storage_info['hostName'],
            storage_info['containerName'],
            storage_info['blobName'],
            storage_info['sasToken']
        )
        print(sas_url)

        with BlobClient.from_blob_url(sas_url) as blob_client:
            with open(file_path, "rb") as f:
                print("saving")
                result = blob_client.upload_blob(f, overwrite=True,
                                                 content_settings=ContentSettings(content_type='image/jpeg'))
                print(result)

        event_payload = {"blob_name": storage_info['blobName'], "device_key": device_key}
        await event_hub_helper.send_event("verification-request-event", event_payload)
        return True, "success"
    except FileNotFoundError:
        return False, "File Not Found."
    except Exception as ex:
        print(ex)
        return False, ex
    finally:
        await device_client.shutdown()


if __name__ == "__main__":
    print(asyncio.run(upload_img_from_device(DEVICE_CONN_STR, DEVICE_KEY, PATH_OF_FILE)))
