from sqlalchemy.orm import Session
from data.models import *
from sqlalchemy.dialects.postgresql import UUID


def get_secret_key(db: Session):
    return db.query(SecretKey).first()

def insert_secret_key(db: Session, skey: str):
    skey_item = SecretKey(id=1, skey=skey, counter=0)
    db.add(skey_item)
    db.commit()
    db.refresh(skey_item)
    return skey_item

def update_secret_key(db: Session, skey: str):
    skey_item: SecretKey = db.query(SecretKey).get(1)
    skey_item.hashed_skey = skey
    skey_item.counter = 0
    db.commit()
    db.refresh(skey_item)
    return skey_item

def get_otp_data(db: Session, uuid_:UUID):
    return db.query(OTPdata).filter_by(unique_id=uuid_).first()

def create_otp_data(db: Session, otp_data: OTPdata):
    db.add(otp_data)
    db.commit()
    db.refresh(otp_data)
    return otp_data

def update_otp_data(db: Session, otp_data: OTPdata):
    current_otp = db.query(OTPdata).filter_by(unique_id=otp_data.unique_id).first()
    current_otp = otp_data
    db.commit()
    db.refresh(current_otp)
    return current_otp

def increment_skey_counter(db: Session):
    skey_item: SecretKey = db.query(SecretKey).get(1)
    skey_item.counter += 1
    db.commit()
    db.refresh(skey_item)
    return skey_item
