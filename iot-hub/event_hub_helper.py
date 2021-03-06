import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import pickle

EVENT_HUB_STRING = "Endpoint=sb://cs5412-final-project-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=+Q23YiwBj5SykbMV4S79zjNQ4r58HCGAKYs2o3f1bvg="


async def send_event(event_hub_name: str, payload, conn_str: str = EVENT_HUB_STRING, serialization: bool = True):
    """
        send an event to an event hub
    :param serialization:
    :param event_hub_name: name of event hub
    :param payload: payload data, must be a dict here
    :param conn_str: connection string of the event hub (must have sending authorization)
    :return: [T / F, message / exception]
    """
    try:
        producer = EventHubProducerClient.from_connection_string(conn_str=conn_str, eventhub_name=event_hub_name)
        async with producer:
            event_data_batch = await producer.create_batch()
            if serialization:
                payload = pickle.dumps(payload)
            event_data_batch.add(EventData(payload))
            await producer.send_batch(event_data_batch)
        return True, "success"
    except Exception as ex:
        return False, ex


if __name__ == "__main__":
    # event_body = {'device_id': "gates-hall-g01",
    #               'blob_name': "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg",
    #               'unit_id': "62475aaadd78bdc4e2448eb8"}
    res_event_body = {'timestamp': 1649651613.762,
                      'unit_id': '62475aaadd78bdc4e2448eb8',
                      'device_id': 'gates-hall-g01',
                      'blob_name': 'gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg',
                      'verified': False,
                      'verify_identity': 'Stranger',
                      'reference_img': None,
                      'confidence': 0.0}
    tenant_blob = "tenants/6251ed05f429e641197c1a37/ebca445b-be87-407d-8267-5bdce0a65c95.png"
    guest_blob = "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg"
    event_body = {"device_key": "ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4=",
                      "blob_name": tenant_blob}


    # res = asyncio.run(send_event("verification-request-event", event_body))
    # res = asyncio.run(send_event("write-records-event", res_event_body))

    # res = asyncio.run(send_event("test-event", event_body))
    # res = asyncio.run(send_event("notify-iot-device-event", res_event_body))
    res = asyncio.run(send_event("send-emails-event", res_event_body))

    print(res)
