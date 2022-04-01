from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
from ..config import azureFaceEndpoint, azureFaceKey

face_client = FaceClient(azureFaceEndpoint, CognitiveServicesCredentials(azureFaceKey))


def get_faceId_with_url(url: str):
    """
    analyze an image using Azure Face, and return the face ID of that image (if a face exists)
    :param url: url of image
    :return: faceID (if there is a face), or None of there isn't
    """
    try:
        detected_faces = face_client.face.detect_with_url(url)
        if not detected_faces:
            return None
        face_id = detected_faces[0].face_id
        return face_id
    except Exception as ex:
        return ex


def get_faceId_with_stream(stream):
    """
    analyze an image using Azure Face and return the face ID
    :param stream:
            1) when using local files, use open(FILE_PATH, "rb")
            2) when using data from Blob storage, wrap the data with
                BytesIO(DATA_READ_FROM_BLOB)
    :return: face ID (if exists), otherwise return None
    """
    try:
        detected_faces = face_client.face.detect_with_stream(stream)
        if not detected_faces:
            return None
        face_id = detected_faces[0].face_id
        return face_id
    except Exception as ex:
        return ex


if __name__ == "__main__":
    print(azureFaceKey)
