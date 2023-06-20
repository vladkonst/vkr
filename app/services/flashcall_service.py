from requests import post
from services.config import settings
from .config import settings

def get_auth_token():
    url = 'https://acallapi3.telediscount.ru/auth/login'
    data = {'email': settings.api_email, 'password': settings.api_pswd}
    r = post(url, data=data)
    return r.json()['token']

def send_flashcall(phone_number: str, otp: str):
    url = 'https://acallapi3.telediscount.ru:443/call-password/start-password-call'
    data = {'async': '1', 'dstNumber': phone_number, 'timeout': '30', 'pin': otp}
    headers = {'Authorization':f'Bearer {settings.api_token}'}
    r = post(url, data=data, headers=headers)
    if r.status_code == 401:
        api_token = get_auth_token()
        settings.api_token = api_token
        r = post(url, data=data, headers=headers)
    if r.status_code == 200:
        return {'message': 'success', 'status': 200, 'call_details': r.json()['callDetails']}
    if r.status_code // 100 == 5:
        return {'message': 'provider server is unreachable', 'status': r.status_code}
    return r.json()
        
        

def get_flashcall_status(call_id: str):
    url = 'https://acallapi3.telediscount.ru:443/call-password/get-password-call-status'
    data = {'callId': call_id}
    r = post(url, data=data)