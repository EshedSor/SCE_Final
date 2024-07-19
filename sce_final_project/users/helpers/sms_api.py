import os
import requests
import json
from django.conf import settings
from datetime import datetime

#-------------------------------------------------------#

def generate_api_token():
    endpoint = settings.SMS_API_ENDPOINT
    req_json = {
    "getApiToken": {
        "user": {
            "username": settings.SMS_API_USERNAME,
            "password": settings.SMS_API_PASSWORD
            },
        "username": settings.SMS_API_USERNAME,
        "action": "new"
        }
    }
    res = requests.post(endpoint, json=req_json)
    if res.status_code == 200:
    # Attempt to parse JSON only if response is OK
        try:
            res_json = res.json()
            return (res_json['message'],res_json['expiration_date'])
        except requests.exceptions.JSONDecodeError:
        # Handle JSON parsing error (e.g., logging, return a default value, etc.)
            print("JSON Decode Error")
    else:
        print("Failed request with status code:", res.status_code)
        # Handle non-200 responses accordingly

#-------------------------------------------------------#
        
def get_api_token():
    try:
        with open('api_token.json', 'r') as openfile:
            json_object = json.load(openfile)
        print("succesfully read from token file")
        return json_object
    except:
        print("Error reading from token file")
        return None

#-------------------------------------------------------#
    
def set_api_token():
    try:
        to_write = generate_api_token()
        with open("api_token.json","w") as outfile:
            json.dump(to_write,outfile)
        print("succesfully written token to file")
    except:
        print("error writing token to file")

#-------------------------------------------------------#
        
def is_token_expired():
    #try:
        json = get_api_token()
        expiration = json[1]
        date_obj = datetime.strptime(expiration, "%d/%m/%Y %H:%M:%S")
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
        if current_datetime>date_obj:
            return True
        return False
    #except:
    #    print("Failed to compare tokens/get token")
    #    return True

#-------------------------------------------------------#

def refresh_token():
    if is_token_expired():
        set_api_token()
    return get_api_token()

#-------------------------------------------------------#
#TEST
def send_sms(phone,otp_code):
    test_API = "https://019sms.co.il/api"
    header =  {"Authorization":settings.SMS_API_TOKEN}
    to_send = {
                "sms": {
                    "user": {
                    "username": settings.SMS_API_USERNAME
                    },
                    "source": settings.SMS_SOURCE_NUMBER,
                    "destinations": {
                    "phone": [phone]
                    },
                    "message": "הסיסמה החד פעמית לצורך התחברות היא  \n {0} \n תוקף הסיסמה 5 דקות".format(otp_code),
                    "includes_international": "0"
                }
            }
    res = requests.post(test_API, json=to_send,headers=header)
    print(res.text)
    return res.json()
