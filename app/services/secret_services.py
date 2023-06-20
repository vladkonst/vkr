import base64
import pyotp
from data.crud import insert_secret_key, update_secret_key, get_secret_key
from sqlalchemy.dialects.postgresql import UUID


def generate_secret() -> str:
    return pyotp.random_base32()

def insert_secret_in_db(SessionLocal):
    with SessionLocal() as session:
        skey = generate_secret()
        insert_secret_key(session, skey)


def update_secret_in_db(SessionLocal):
    with SessionLocal() as session:
        skey = get_secret_key(session)
        if not skey:
            insert_secret_in_db(SessionLocal)
        else:
            skey = generate_secret()
            update_secret_key(session, skey)

def modificate_secret(uuid: UUID, phone_digits: str, skey: str):
    uuid_ = ''.join(str(uuid).split('-'))
    modification = str.encode(uuid_ + phone_digits)
    modification_b32 = base64.b32encode(modification)
    skey_modificated = skey + modification_b32.decode()
    return skey_modificated


