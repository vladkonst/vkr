import pyotp
from datetime import datetime, timedelta
from services.secret_services import modificate_secret
from data.crud import increment_skey_counter, update_otp_data, create_otp_data
from hashlib import sha256
from data.models import *
from data.schemes import UserData
from sqlalchemy.orm import Session


def otp_generate(db: Session,skey: SecretKey, otp_data: OTPdata, user_data: UserData):
    modificated_skey = modificate_secret(otp_data.unique_id, user_data.phone_number[-3:], skey.skey)
    hotp = pyotp.HOTP(modificated_skey, digits=4)
    otp = hotp.at(skey.counter + otp_data.gen_try_count)
    increment_skey_counter(db)
    return otp

def retrieve_hashed_otp(otp):
    hfunc = sha256()
    hfunc.update(otp.encode())
    hashed_otp = hfunc.hexdigest()
    return hashed_otp

def otp_update(flag, db: Session, otp_data: OTPdata, user_data: UserData, skey: SecretKey):
    if not flag:
        otp_data.gen_try_count = 0
    otp_data.experation_time = datetime.now() + timedelta(minutes=15)
    otp = otp_generate(db, skey, otp_data, user_data)
    otp_data.hashed_otp = retrieve_hashed_otp(otp)
    otp_data.gen_try_count += 1
    update_otp_data(db, otp_data)
    return otp

def otp_update_call_id(db: Session, otp_data: OTPdata,call_id:str):
    otp_data.call_id = call_id
    update_otp_data(db, otp_data)

def update_valid_try_count(db: Session, otp_data: OTPdata):
    otp_data.valid_try_count += 1
    update_otp_data(db, otp_data)

def update_verified(db: Session, otp_data: OTPdata):
    otp_data.verified = True
    update_otp_data(db, otp_data)

def otp_create(db: Session, user_data: UserData, skey: SecretKey):
    experation_time = datetime.now() + timedelta(minutes=15)
    otp_data = OTPdata(unique_id=user_data.UUID, verified=False, gen_try_count=1, valid_try_count=0, experation_time=experation_time)
    otp = otp_generate(db, skey, otp_data, user_data)
    otp_data.hashed_otp = retrieve_hashed_otp(otp)
    create_otp_data(db, otp_data)
    return otp