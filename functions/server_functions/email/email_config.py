EMAIL_SUBJECTS = {
    "register_token": "[CS5412-CL2228] Account Register Token",
    "retrieve_token": "[CS5412-CL2228] Account Retrieve Token",
    "warning_record": "[CS5412-CL2228] Suspicious Entrance Record of Your Apartment"
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
    "warning_record":
        """Dear user {},

There is a suspicious record in your unit {} , {} at {}. Please Login to the system to check the entrance record.

Thanks,
CL 
""",
    "warning_html": """
    <html>
    <body>
    Dear user, </br></br>
    There is a suspicious entrance record of your apartment <b>{}, {}</b> at <i>{}</i>. 
    Here is the photo taken from this record. Please log in to our system to check if action needed.</br></br>
    Thanks.</br>
    CL<br>
    <img src="{}"></br>.
    </body>
    </html>
    """
}


ALLOW_TYPES = {"register_token", "retrieve_token"}


if __name__ == "__main__":
    unit_data = {
        "unit_name": "Apt 6",
        "building_name": "612 E Buffalo St"
    }

    msg = EMAIL_BODIES['warning_record'].format("cl2228@cornell.edu",
                                                unit_data['unit_name'],
                                                unit_data['building_name'],
                                                123)
