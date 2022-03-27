import logging
import azure.functions as func

from ..helpers import azure_face_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )

    face_url = req.params.get('face-url')
    if not face_url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            face_url = req_body.get("face-url")
    
    if face_url:
        face_id = azure_face_helpers.get_faceId_with_url(face_url)
        if face_id == None:
            return func.HttpResponse(
                "No face detected",
                status_code=200
            )

        response_str = "face detected with faceID:{}".format(face_id)
        return func.HttpResponse(response_str)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a URL in the query string or in the request body for a personalized response.",
             status_code=200
        )
