from sqlalchemy.orm import Session
from data.crud import get_otp_data
from services.otp_services import retrieve_hashed_otp, update_valid_try_count, update_verified
from data.models import OTPdata
from data.schemes import ValidationData
from datetime import datetime


def validate_token(validation_data:ValidationData, db: Session):
    otp_data: OTPdata = get_otp_data(db, validation_data.UUID)
    
    if otp_data:
        flag = otp_data.experation_time > datetime.now()
        if flag:
            if not otp_data.verified:
                if otp_data.valid_try_count < 3:
                    hashed_otp = retrieve_hashed_otp(validation_data.otp)
                    if hashed_otp == otp_data.hashed_otp:
                        update_verified(db, otp_data)
                        return {'message':'validated', 'status':200}
                    update_valid_try_count(db, otp_data)
    return {'message':'not validated', 'status':405}
