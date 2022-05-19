from typing import Optional
from datetime import datetime, timedelta
import os
import requests
import time
import webbrowser

from .constants import CLIENT_ID, AUDIENCE

# all API call headers
HEADERS = {
    'content-type': 'application/x-www-form-urlencoded',
}

# device code API call body
DEVICE_BODY = {
    "client_id": os.environ[CLIENT_ID],
    "audience": os.environ[AUDIENCE]
}

# access token API call body
ACCESS_BODY = {
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    "client_id": os.environ[CLIENT_ID]
}

#Perform OAuth 2.0 Device auth procedure
def oauth() -> Optional[str]:    
    res = requests.post("https://dev-1ky8c6vy.us.auth0.com/oauth/device/code", headers=HEADERS, data=DEVICE_BODY)
    try:
        res.raise_for_status()
    except Exception as e:
        print(e)
        return None
    
    res_json = res.json()
    
    try:
        user_code = res_json["user_code"]
        interval = res_json["interval"]
        verification_url = res_json["verification_uri_complete"]
        
        ACCESS_BODY["device_code"] = res_json["device_code"]
    except KeyError as ke:
        print(f"Auth0 response invalid: {ke}")
        return None
    
    print(f"Please visit {verification_url} using a browser and login/sign up.")
    print(f"Confirmation code is {user_code}.")
    
    # open link in browser if possible
    webbrowser.open_new(verification_url)
    
    # wait 5 minutes (interval = 5 seconds usually)
    for _ in range(60):
        time.sleep(interval)
        
        res = requests.post("https://dev-1ky8c6vy.us.auth0.com/oauth/token", headers=HEADERS, data=ACCESS_BODY)
        res_json = res.json()
        
        if (res.status_code == 200):
            token = res_json["access_token"]
            expiry = res_json["expires_in"]
            
            with open("./token_cache.txt", "w") as file:
                file.write(token + "\n")
                file.write(str(datetime.now() + timedelta(seconds=expiry)))
                
            return token

        if (res_json["error"] != "authorization_pending"):
            print(res_json["error_description"])
            return None
        
    print("Time limit of 5 minutes exceeded, exiting.")
    return None
      
if (__name__ == "__main__"):
    print(oauth())
    