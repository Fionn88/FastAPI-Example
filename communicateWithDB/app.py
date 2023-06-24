
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import List
from pydantic import BaseModel

# Using MySQL
DATABASE_URL = "mysql+mysqlconnector://root:0624@localhost:3306/fastapi"
# DATABASE_URL = "mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_IP}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()

class Books(Base):
   __tablename__ = 'book'
   id = Column(Integer, primary_key=True, nullable=False)
   title = Column(String(50), unique=True)
   author = Column(String(50))
   publisher = Column(String(50))
   Base.metadata.create_all(bind=engine)

class Book(BaseModel):
   id: int
   title: str
   author:str
   publisher: str
   class Config:
      orm_mode = True

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/add_new', response_model=Book)
def add_book(b1: Book, db: Session = Depends(get_db)):
   bk=Books(id=b1.id, title=b1.title, author=b1.author,
publisher=b1.publisher)
   db.add(bk)
   db.commit()
   db.refresh(bk)
   return Books(**b1.dict())

@app.get('/list', response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
   recs = db.query(Books).all()
   return recs

@app.get('/book/{id}', response_model=Book)
def get_book(id:int, db: Session = Depends(get_db)):
   return db.query(Books).filter(Books.id == id).first()

@app.put('/update/{id}', response_model=Book)
def update_book(id:int, book:Book, db: Session = Depends(get_db)):
   b1 = db.query(Books).filter(Books.id == id).first()
   b1.id=book.id
   b1.title=book.title
   b1.author=book.author
   b1.publisher=book.publisher
   db.commit()
   return db.query(Books).filter(Books.id == id).first()

@app.delete('/delete/{id}')
def del_book(id:int, db: Session = Depends(get_db)):
   try:
      db.query(Books).filter(Books.id == id).delete()
      db.commit()
   except Exception as e:
      raise Exception(e)
   return {"delete status": "success"}