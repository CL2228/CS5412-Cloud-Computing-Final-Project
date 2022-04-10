from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
from ..config import azureFaceEndpoint, azureFaceKey
# from functions.server_functions.config import azureFaceEndpoint, azureFaceKey

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
            return False, "No face detected"
        face_id = detected_faces[0].face_id
        return True, str(face_id)
    except Exception as ex:
        return False, str(ex)


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
            return False, "No face detected"
        face_id = detected_faces[0].face_id
        return True, str(face_id)
    except Exception as ex:
        return False, str(ex)


def verify_two_faces(face_id_1: str, face_id_2: str):
    """
    verify two faces based on their face IDs
    :param face_id_1: str, face ID
    :param face_id_2: str, face ID
    :return: [T / F, confidence / exception]
    """
    try:
        result = face_client.face.verify_face_to_face(face_id_1, face_id_2)
        return result.is_identical, result.confidence
    except Exception as ex:
        return False, str(ex)


if __name__ == "__main__":
    res = get_faceId_with_url("http://localhost:7071/api/img-get?name=gates-hall-g01/records/69a20fb2-6442-4fa6-ba6f-4bc02d4afeff.jpg")
    print(res)
