# **Azure HTTP function Module**
> This module is the core of this CS5412 final project. It contains **HTTP** serverless functions that suppor the central functionality of the project. Note that **only functions that receive HTTP requests** are included in this page because they are called by the frontend. Other functions that triggered by other Azure modules such as ***IoT Hub, Azure Event Hub*** are not opened to public frontends.

## **Run this module**
> There is **no need** for you to configure this module to run on your local computer or on Azure. All serverless functions are **already running** on Azure. The aim of this page is to provide instructions on how to use APIs I implemented.

## **API Catalog**
- ### [**Register an account**](#register-account)
- ### 


# **API Manual**

# Register Account
## Overall
- This function is used for registering a new account. There are two steps to register account:
    1. The first step is to request the server to send an email token. 
    2. The second step is to provide this received token to verify your email and finish the registration process.
## Request
- ### **URL**: `https://cs5412-final-project.azurewebsites.net/api/user-account-create`