EMAIL_SUBJECTS = {
    "register_token": "[CS5412-CL2228] Account Register Token",
    "retrieve_token": "[CS5412-CL2228] Account Retrieve Token"
}


EMAIL_BODIES = {
    'register_token':
        """Dear user <{}>,

You are creating an account on our website, please use the verification code below to finish the registration.
Please copy and paste the whole token:

{}
    
Thanks,
CL
""",
    'retrieve_token':
        """Dear user,
        
You are retrieving your account <{}>, please use the verification code below to finish the process.
Please copy and paste the whole token:

{}
    
Thanks,
CL
""",

}


ALLOW_TYPES = {"register_token", "retrieve_token"}
