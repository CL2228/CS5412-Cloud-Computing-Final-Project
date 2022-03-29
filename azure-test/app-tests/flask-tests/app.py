import flask
from flask import Flask, request, json
from io import BytesIO

app = Flask(__name__)
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=cs5412finalproject;AccountKey=IY/FhO+zJy+jui2TmIcHKp3uyWEZ/9eAxx/DnSsa0edvVOFIJnJrSiEKLYxUCXUBy8HRieupaXfg+AStBlMzjg==;EndpointSuffix=core.windows.net"


@app.route('/', methods=['GET'])
def index():
    # file = open("../../fundamental-tests/sample.jpg", "rb").read()
    # print(file)
    headers = request.files['file'].stream.read()
    print(headers)
    return headers


@app.route('/img', methods=['GET'])
def get_img():
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service_client.get_container_client("test-container")
    blob_client = blob_service_client.get_blob_client("test-container", "test.jpg")
    blobs = container_client.list_blobs()
    blob_downloader = blob_client.download_blob()
    data = blob_downloader.readall()

    response = flask.Response(data)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@app.route('/test-get', methods=['GET'])
def test_get():
    obj = {
        "name": "Chenghui LI",
        "netID": "cl2228"
    }
    return json.jsonify(obj)


@app.route('/upload', methods=['POST'])
def upload_img():
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service_client.get_container_client("test-container")
    blob_client = blob_service_client.get_blob_client("test-container", "sample.jpg")
    img = BytesIO(open("../../fundamental-tests/sample.jpg", "rb"))


if __name__ == "__main__":
    app.run()
