from sqlalchemy.orm import Session
from data.crud import get_secret_key, get_otp_data
from services.otp_services import otp_update, otp_create, otp_update_call_id
from data.models import SecretKey, OTPdata
from data.schemes import UserData
from datetime import datetime
from services.flashcall_service import send_flashcall


def generate_token(user_data:UserData, db: Session):
    otp_data: OTPdata = get_otp_data(db, user_data.UUID)

    if otp_data:
        skey: SecretKey = get_secret_key(db)
        if not skey:
            return
        flag = otp_data.experation_time > datetime.now()
        if flag:
            if otp_data.gen_try_count >= 3:
                return {'message':'превышено допустимое количество генераций', 'status':405}
        otp = otp_update(flag, db, otp_data, user_data, skey)
    else:
        skey: SecretKey = get_secret_key(db)
        otp = otp_create(db, user_data, skey)
        
    r = send_flashcall(user_data.phone_number, otp)
 
    return r
