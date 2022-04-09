import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition

from blob_test import *

CONTAINER_NAME = "test-container"
BLOB_NAME = "ray-img"

FACE_KEY = "f15b29c9e66b461da5edf600cf819b06"
FACE_ENDPOINT = "https://cs5412-final-project-face-paid.cognitiveservices.azure.com/"

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))


# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return ((left, top), (right, bottom))


def drawFaceRectangles(bytes_data, detected_faces):
    # Download the image from the url
    img = Image.open(bytes_data)

    # For each face returned use the face rectangle and draw a red box.
    print('Drawing rectangle around face... see popup for results.')
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')
    img.show()


if __name__ == "__main__":
    print("running")
    # raw_bytes = read_a_blob(CONTAINER_NAME, BLOB_NAME)
    # img_file = open("./sample.jpg", "rb")
    # io_bytes = BytesIO(raw_bytes)
    # print(face_client)

    # face_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
    # detected_faces = face_client.face.detect_with_stream(image=io_bytes)
    # if not detected_faces:
    #     raise Exception("No face detected")
    # for face in detected_faces:
    #     print('Detected face ID:  {}'.format(face.face_id))

    # drawFaceRectangles(io_bytes, detected_faces)

    verify_result_diff = face_client.face.verify_face_to_face("f92c9821-fa9a-44c1-80b1-d5aaff4e9976",
                                                              "f92c9821-fa9a-44c1-80b1-d5aaff4e9976")
    print('Faces from {} & {} are of the same person, with confidence: {}'
          .format("face1", "face2", verify_result_diff.confidence)
          if verify_result_diff.is_identical
          else 'Faces from {} & {} are of a different person, with confidence: {}'
          .format("face1", "face2", verify_result_diff.confidence))
