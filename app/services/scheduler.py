import schedule
import time
from data.database import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.secret_services import insert_secret_in_db, update_secret_in_db


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def first_job():
    insert_secret_in_db(SessionLocal)
    return schedule.CancelJob

schedule.every(1).minutes.do(first_job)

def job():
    update_secret_in_db(SessionLocal)

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)