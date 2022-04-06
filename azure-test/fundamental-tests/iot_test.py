# from azure.iot.device.aio import IoTHubDeviceClient
import asyncio
import os
from azure.iot.device import IoTHubDeviceClient
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobClient

CONNECTION_STRING = "HostName=cs5412-final-project-iothub.azure-devices.net;DeviceId=mydevice;SharedAccessKey=zPf2c7/72WJLuogSOw98IbwZtM/qsT/h81KkWyuRjj4="
PATH_TO_FILE = "./sample.jpg"

DEVICE_CONNECTION_STRING = "HostName=cs5412-final-project-iothub.azure-devices.net;DeviceId=mydevice;SharedAccessKey=zPf2c7/72WJLuogSOw98IbwZtM/qsT/h81KkWyuRjj4="


async def func():
    conn_str = DEVICE_CONNECTION_STRING

    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    await device_client.connect()

    print("Sending msg..")
    await device_client.send_message("Test message from LCH")
    print("Sent successfully")

    await device_client.shutdown()


def store_blob(blob_info, file_name):
    try:
        sas_url = "https://{}/{}/{}{}".format(
            blob_info["hostName"],
            blob_info['containerName'],
            blob_info['blobName'],
            blob_info['sasToken']
        )

        print("\nUploading file: {} to Azure storage as blob: {} in container {}\n".format(
            file_name, blob_info['blobName'], blob_info['containerName']
        ))

        with BlobClient.from_blob_url(sas_url) as blob_client:
            with open(file_name, "rb") as f:
                result = blob_client.upload_blob(f, overwrite=True)
                return True, result
    except FileNotFoundError as ex:
        ex.status_code = 404
        return False, ex
    except AzureError as ex:
        return False, ex


def run_sample(device_client):
    # Connect the client
    device_client.connect()

    # Get the storage info for the blob
    blob_name = os.path.basename(PATH_TO_FILE)
    storage_info = device_client.get_storage_info_for_blob(blob_name)

    print(storage_info)

    # Upload to blob
    success, result = store_blob(storage_info, PATH_TO_FILE)

    if success:
        print("Upload succeeded. Result is: \n")
        print(result)
        print()

        device_client.notify_blob_upload_status(
            storage_info["correlationId"], True, 200, "OK: {}".format(PATH_TO_FILE)
        )
    else:
        # If the upload was not successful, the result is the exception object
        print("Upload failed. Exception is: \n")
        print(result)
        print()

        device_client.notify_blob_upload_status(
            storage_info["correlationId"], False, result.status_code, str(result)
        )


def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # device_client.connect()
    # storage_info = device_client.get_storage_info_for_blob("xio.png")
    # print(storage_info)

    try:
        print("IoT Hub file upload sample, press Ctrl-C to exit")
        run_sample(device_client)
    except KeyboardInterrupt:
        print("IoTHubDeviceClient sample stopped")
    finally:
        # Graceful exit
        device_client.shutdown()


if __name__ == "__main__":
    main()

