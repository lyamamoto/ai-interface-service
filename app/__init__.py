from dotenv import load_dotenv
load_dotenv()

import os
sqlalchemy_url = f"postgresql+psycopg2://{os.getenv('postgres.user')}:{os.getenv('postgres.password')}@{os.getenv('postgres.host')}/{os.getenv('postgres.db')}"

from sqlalchemy import create_engine
engine = create_engine(sqlalchemy_url)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class AuthException(Exception):
    def __init__(self, message="Customer not found for auth token"):
        self.message = message
        super().__init__(self.message)

from .application import app