# **Azure Function HTTP Module**
> This module is the core of this CS5412 final project. It contains **HTTP** serverless functions that suppor the central functionality of the project. Note that **only functions that receive HTTP requests** are included in this page because they are called by the frontend (why you need these instructions). Those functions that triggered by other Azure modules such as ***IoT Hub, Azure Event Hub*** are not opened to public frontends.

## **Run this module**
> There is **no need** for you to configure this module to run on your local computer or on Azure. All serverless functions are **already running** on Azure. The aim of this page is to provide instructions on how to use APIs I implemented.

## **API Catalog**
- ### [**User Register an account**](#register-account)
- ### [**User login**](#log-in)
- ### [**User Change Password**](#change-password)
- ### [**User Change Verification Photo**](#change-verification-image)
- ### [**User Add Unit**](#add-unit)
- ### [**User Add Guests**](#add-guest)
- ### [**User Get Records**](#get-records)
- ### [**Get image from the system**](#get-image)
- ### [**User Dashboard**](#dashboard)
# **API Manual**

****

# Register Account
## Overall
- This function is used for registering a new account. There are two steps to register account:
    1. The first step is to request the server to send an email token. 
    2. The second step is to provide this received token to verify your email and finish the registration process.
## Request
- ### **URL**: 
    `POST` `https://cs5412-final-project.azurewebsites.net/api/user-account-create`
- ### **Headers**:
    - `Content-Type`: `"application/json"`
- ### **Body**: A JSON body should be provided
    - `req-type`: the type of the request. In this API there are two types: `"send_token"` and `"verify"`. Each represents the step of the process.
    - `email`: the email of the new account.
    - `password`: the password of this new account. **Only required in the `verify` request type**.
    - `first-name`: the first name of this new account. **Only required in the `verify` request type**.
    - `last-name`: the last name of this new account. **Only required in the `verify` request type**.
    - `token`: the token that was sent to the email. **Only required in the `verify` request type**.
- ### **Sample request body**:
    ```json
    {
        "req-type": "send_token",
        "email": "example@example.com"
    }
    ```
    ```json
    {
        "req-type": "verify",
        "email": "example@example.com",
        "password": "12345678",
        "first-name": "Chenghui",
        "last-name": "Li",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJlbWF"
    }
    ```
## Response:
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
- ### Request failures:
    - `400`: Usually result from wrong request format.
    - `401`: Wrong or invalid token provided.
    - `403`: Account already existed.
    - `500`: Internal errors, might be because lost connection to database.

****

# Log in
## Overall
- This function is used for user longin. After log in successfully, a JWT will be returned. This token needs to be stored in frontend as it is necessary for all user operations.
## Request:
- ### **URL**:
    `POST` `https://cs5412-final-project.azurewebsites.net/api/user-account-login`
- ### **Headers**: 
    - `Content-Type`: `"application/json"`
- ### **Body**: A JSON body should be provided
    - `email`: the email of the account.
    - `password`: password.
## Response:
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
    - `access-token`: the token for authentication, should be kept in the browser locally.
    - `data`: the information of the account
        - `email`: email
        - `first_name`: first name
        - `last_name`: last name
        - `face_img`: the blob name of this user's verification image
        - `units`: this user's unit information
- ### Request failures:
    - `400`: Wrong request format.
    - `401`: Wrong password.
    - `404`: User not found.
    - `500`: Internal errors.
- ### **Sample response body**:
    ```json
    {
        "access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
        "data": {
            "email": "cl2228@cornell.edu",
            "first_name": "Chenghui",
            "last_name": "Li",
            "face_img": "tenants/6251ed05f429e641197c1a37/ebca445b-be87-407d-8267-5bdce0a65c95.png",
            "units": {
                "62475aaadd78bdc4e2448eb8": {
                    "building_name": "GatesHall",
                    "unit_number": "G01"
                }
            }
        }
    }
    ```

****

# Change Password:
## Overall
- This function is used for resetting the password of an account. Similar to register an account, there are two steps:
    1. The first step is to send a token to the email for verification.
    2. The second step is to verify the token and reset the password
## Request
- ### **URL**:
    `POST` `https://cs5412-final-project.azurewebsites.net/api/user-account-update-pswd`
- ### **Headers**:
    - `Content-Type`: `"application/json"`
- ### **Body**: A JSON body should be provided
    - `req-type`: the type of the request. In this API there are two types: `"send_token"` and `"verify"`. Each represents the step of the process.
    - `email`: the email of the new account.
    - `new-password`: the new password of this new account. **Only required in the `verify` request type**.
    - `token`: the token that was sent to the email. **Only required in the `verify` request type**.
- ### **Sample request body**:
    ```json
    {
        "req-type": "send_token",
        "email": "example@example.com"
    }
    ```
    ```json
    {
        "req-type": "verify",
        "email": "example@example.com",
        "new-password": "12345678",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJlbWF"
    }
    ```
## Response
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
- ### Request failures:
    - `400`: Usually result from wrong request format.
    - `401`: Wrong or invalid token provided.
    - `404`: Account not found.
    - `500`: Internal errors. Might be concurrent write for the same account to the database.

****

# Change verification image
## Overall
- This function is used for changing the verification photo of tenants. When first creating a new account, **there is no verification image by defult**. The user needs to change his/her photo so that they can be approved when entering his/her apartment. The frontend should call this API for this purpose.
## Request
- ### **URL**:
    `POST`: `https://cs5412-final-project.azurewebsites.net/api/user-account-update-img`
- ### **Headers**
    - `Content-Type`: `"multipart/from-data"`
    - `x-access-token`: the token received from the login process.
- ### **Body**: A Multi-part Form body should be provided
    - `img`: the verification image of the tenant. Support type: jpg/jpeg/png. This image must contain the tenant's face.
## Response
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
- ### Request failures:
    - `400`: Usually result from wrong request format. This might be missing token, missing form fileds, unsupported image file format, the size of the image is too big, or a multipart/form body is not used.
    - `401`: Wrong or invalid token provided.
    - `403`: There is no face in the uploaded image.
    - `404`: Account does not exist.
    - `500`: Internal failures. Might be because failed Blob Storage connection, or concurrent write to database, etc.

****

# Add Unit
## Overall
- A user can have more than one unit (for example, he/she is rich). When first register a new account, this account doesn't have any unit, so the user needs to add his/her apartments to his account. Before adding a unit, the user needs to obtain a UnitID from the building leasing office.
## Request
- ### **URL**:
    `POST`: `https://cs5412-final-project.azurewebsites.net/api/user-add-unit`
- ### **Headers**
    - `Content-Type`: `"application/json`
    - `x-access-token`: the token received from the login process.
- ### **Body**: A JSON body should be provided
    - `unit-id`: the ID of the unit.
## Response
- ### A JSON is returned
- `message`: A message that indicates the status of this query, no matter succeed or not.
- ### Request failures:
    - `400`: Usually result from wrong request format. 
    - `401`: The access token is not valid.
    - `403`: This account has already added this unit.
    - `404`: Unit or tenant account not found.
    - `500`: Internal errors. Might be because concurrent write to the same unit/tenant account.

****

# Add Guest
## Overall
- A tenant can add temporary guests to his/her apartments. When adding guests, the tenant needs to specify the first name and last name of the guest, as well as the unit ID, and a photo that contains the face of that guest.
## Request
- ### **URL**
    `POST` `https://cs5412-final-project.azurewebsites.net/api/user-add-guest`
- ### **Headers**
    - `Content-Type`: `"multipart/from-data"`
    - `x-access-token`: the token received from the login process.
- ### **Body**: A Multi-part Form body should be provided
    - `img`: the verification image of the guest. Support type: jpg/jpeg/png. This image must contain the guest's face.
    - `first-name`: the first name of the guest.
    - `last-name`: the last name of the guest.
    - `unit-id`: the unit ID of the aprtment that the guest is going to visit.
## Response
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
- ### Request failures:
    - `400`: Usually result from wrong request format. This might be missing token, missing form fileds, unsupported image file format, the size of the image is too big, or a multipart/form body is not used.
    - `401`: The token is not valid. Or this tenant has no right to the unit.
    - `403`: No face is detected or the size of image is too big.
    - `404`: No tenant account found or the unitID is not valid.
    - `500`: Internal errors. 

****

# Get Records
## Overall
- A tenant can retrieve and inspect entrance records of his/her apartments. To use this API to fetch records, the tenant needs to provide right access token (received when login) and the correct unit ID.
## Request
- ### **URL**
    `GET` `https://cs5412-final-project.azurewebsites.net/api/user-get-records`
- ### **Headers**
    - `Content-Type`: `"application/json"`
    - `x-access-token`: the token received from the login process.
- ### **Body**: A JSON body should be provided
    - `unit-id`: the ID of the unit.
## Response
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
    - `data`: A list that contains records. Records are sorted by the timestamps, from newest to oldest. The format of each piece of data:
        - `timestamp`: the timestamp of this entrance record (UTC timezone, London).
        - `face_img`: the blob name of the image of this entrance record. The image is taken when the vistor initiated a entrance request at the IoT edge.
        - `verified`: This entrance record is verified or not.
        - `verify_identity`: The name of matched tenant/guest of this entrance record. If no matched person found, this field will be `Stranger`.
        - `ref_img`: the blob name of the reference image of this visitor. Reference image only exists when the system finds a matched person in the system (this person can be a tenant or a guest). When no matched person found (the visitor is a stranger), this field will be `null`.
- ### Request failures:
    - `400`: Wrong request format.
    - `401`: Wrong JWT token or the tenant doesn't have authorization to check the entrance records of this unit.
    - `404`: No unitId is found, or there is no such tenant user in the system.
    - `500`: Internal errors.
- ### **Sample reponse**
    ```json
    {
        "data": [
            {
                "timestamp": 1649818577.37,
                "face_img": "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg",
                "ref_img": null,
                "verified": false,
                "verify_identity": "Stranger"
            },
            {
                "timestamp": 1649818533.152,
                "face_img": "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg",
                "ref_img": null,
                "verified": false,
                "verify_identity": "Stranger"
            },
            {
                "timestamp": 1649817814.377,
                "face_img": "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg",
                "ref_img": null,
                "verified": false,
                "verify_identity": "Stranger"
            }
        ],
        "message": "Success"
    }
    ```

****

# Get Image
## Overall
- This is a image-based system, which verifiees the validity of entrance request by visitor's images taken by IoT edge devices. This API is provided for querying images from the system.
## Request
- ### **URL**
    `GET` `https://cs5412-final-project.azurewebsites.net/api/img-get`
- ### **Params**
    - `name`: the blob name of the image.
- ### **Sample request URL**
    `GET` `https://cs5412-final-project.azurewebsites.net/api/img-get?name=gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg`
## Response
- ### If data found, a byte vector contains image data is returned. If not, a JSON is returned and the field `message` contians the error message.
- ### Request failures:
    - `400`: Wrong request format, mainly because missing `name` filed in params.
    - `404`: No data found. You need to check the blob name.

****

# Dashboard
## Overall
- This API is developed for getting dashboard information of a tenant. Tenant's data and his/her units' five most recent entrance records are returned.
- ### **URL**
    `GET` `https://cs5412-final-project.azurewebsites.net/api/user-dashboard`
- ### **Headers**
    - `x-access-token`: the token received from the login process.
## Response
- ### A JSON is returned
- ### JSON fields:
    - `message`: A message that indicates the status of this query, no matter succeed or not.
    - `data`: An dict that contains the tenant data and records of his/her units
        - `tenant`: a dict that contains the basic information about the user tenant
        - `units`: a list that contains all units that this tenant has, each piece of data contains:
            - `unit`: the unit information.
            - `records`: five most recent entrance records of this unit.
- ### Request failures:
    - `400`: Usually result from wrong request format. This might be missing token, missing form fileds, unsupported image file format, the size of the image is too big, or a multipart/form body is not used.
    - `401`: The token is not valid. Or this tenant has no right to the unit.
    - `404`: No tenant account found.
    - `500`: Internal errors. 
- ### **Sample response**:
    ```json
    {
        "data": {
            "tenant": {
                "email": "cl2228@cornell.edu",
                "first_name": "Chenghui",
                "last_name": "Li",
                "face_img": "tenants/6251ed05f429e641197c1a37/ebca445b-be87-407d-8267-5bdce0a65c95.png",
                "units": {
                    "62475aaadd78bdc4e2448eb8": {
                        "building_name": "GatesHall",
                        "unit_number": "G01"
                    }
                }
            },
            "units": [
                {
                    "unit": {
                        "building_name": "GatesHall",
                        "address": "Cornell University",
                        "unit_number": "G01",
                        "tenants": {
                            "cl2228@cornell.edu": "6251ed05f429e641197c1a37"
                        }
                    },
                    "records": [
                        {
                            "timestamp": 1650311531.197,
                            "face_img": "gates-hall-g01/records/1eda61e0-4b71-4988-a7f4-832cf5553ad1.jpg",
                            "ref_img": null,
                            "verified": false,
                            "verify_identity": "Stranger"
                        },
                        {
                            "timestamp": 1650166130.593,
                            "face_img": "gates-hall-g01/records/ee11dd9f-26d3-404f-a100-d2572dc6e0f7.jpg",
                            "ref_img": null,
                            "verified": false,
                            "verify_identity": "Stranger"
                        },
                        {
                            "timestamp": 1650161591.104,
                            "face_img": "gates-hall-g01/records/653341e9-7b6f-409c-8b5b-01a603db8dfd.jpg",
                            "ref_img": null,
                            "verified": false,
                            "verify_identity": "Stranger"
                        },
                        {
                            "timestamp": 1650161401.851,
                            "face_img": "gates-hall-g01/records/3e5fc0c6-8181-48cf-8820-ca407e54860d.jpg",
                            "ref_img": null,
                            "verified": false,
                            "verify_identity": "Stranger"
                        },
                        {
                            "timestamp": 1650158360.741,
                            "face_img": "gates-hall-g01/records/f6f4ed64-a960-4f3d-8b62-fd7ff4b5cb99.jpg",
                            "ref_img": null,
                            "verified": false,
                            "verify_identity": "Stranger"
                        }
                    ]
                }
            ]
        },
        "message": "Success"
    }
    ```