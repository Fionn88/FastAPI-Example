from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Using MySQL
DATABASE_URL = "mysql+mysqlconnector://root:0624@localhost:3306/fastapi"
# DATABASE_URL = "mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_IP}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

