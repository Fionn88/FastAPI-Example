from sqlalchemy.schema import Column
from sqlalchemy import Column, Integer, String
from database import Base
class Books(Base):
   __tablename__ = 'book'
   id = Column(Integer, primary_key=True, nullable=False)
   title = Column(String(50), unique=True)
   author = Column(String(50))
   publisher = Column(String(50))
