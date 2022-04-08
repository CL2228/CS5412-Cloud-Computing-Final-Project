import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import pickle

EVENT_HUB_STRING = "Endpoint=sb://cs5412-final-project-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=+Q23YiwBj5SykbMV4S79zjNQ4r58HCGAKYs2o3f1bvg="


async def send_event(event_hub_name: str, payload, conn_str: str = EVENT_HUB_STRING, ):
    try:
        producer = EventHubProducerClient.from_connection_string(conn_str=conn_str, eventhub_name=event_hub_name)
        async with producer:
            event_data_batch = await producer.create_batch()
            event_body = pickle.dumps(payload)
            event_data_batch.add(EventData(event_body))
            await producer.send_batch(event_data_batch)
        return True, "success"
    except Exception as ex:
        return False, ex

if __name__ == "__main__":
    pass