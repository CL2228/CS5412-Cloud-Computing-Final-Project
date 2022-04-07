import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import pickle
EVEN_HUB_STRING = "Endpoint=sb://cs5412-final-project-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=+Q23YiwBj5SykbMV4S79zjNQ4r58HCGAKYs2o3f1bvg="

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str= EVEN_HUB_STRING, eventhub_name="test-event")
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        body = pickle.dumps({"message": "xio"})
        event_data_batch.add(EventData(body))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())