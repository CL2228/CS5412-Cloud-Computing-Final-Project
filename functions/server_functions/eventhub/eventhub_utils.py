from ..config import eventHubRootConnectionString
from azure.eventhub import EventHubProducerClient, EventData
import pickle


def send_event(event_hub_name: str,
               payload,
               conn_str: str = eventHubRootConnectionString,
               serialization: bool = True):
    """
    send event data
    :param event_hub_name: the name of event hub (not eventhub namespace)
    :param payload: the payload of the event data body
    :param conn_str: connection string to the eventhub, this conn_str needs to have "send" authorization
    :param serialization: with / without pickle serialization
    :return: [T / F, message]
    """
    try:
        producer = EventHubProducerClient.from_connection_string(conn_str=conn_str, eventhub_name=event_hub_name)
        event_data_batch = producer.create_batch()
        if serialization:
            payload = pickle.dumps(payload)
        event_data_batch.add(EventData(payload))
        producer.send_batch(event_data_batch)
        return True, "Event data sent"
    except Exception as ex:
        return False, str(ex)
