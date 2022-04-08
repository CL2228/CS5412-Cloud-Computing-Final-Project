from azure.eventhub import EventData
import json
import pickle


if __name__ == "__main__":
    res_body = {"message": "cl2228"}
    res_json = json.dumps(res_body)
    bts = pickle.dumps(res_body)
    print(bts)
    event_data = EventData(bts)
    # print(event_data.body_as_json())
    # print(event_data.enqueued_time)
    print(pickle.loads(bts))
