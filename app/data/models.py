from sqlalchemy import (Boolean, Column, Integer,
    String, SmallInteger, DateTime)
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


class SecretKey(Base):
    __tablename__ = "skeys"

    id = Column(Integer, primary_key=True)
    skey = Column(String)
    counter = Column(Integer)

class OTPdata(Base):
    __tablename__ = "otp_data"
    
    id = Column(Integer, primary_key=True)
    hashed_otp = Column(String)
    unique_id = Column(UUID(as_uuid=True))
    verified = Column(Boolean)
    gen_try_count = Column(SmallInteger)
    valid_try_count = Column(SmallInteger)
    experation_time = Column(DateTime)
    call_id = Column(String)
