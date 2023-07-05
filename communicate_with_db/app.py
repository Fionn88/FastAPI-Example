
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import schema
from database import SessionLocal, engine
import model


app = FastAPI()

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


model.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/add_new', response_model=schema.Book)
def add_book(b1: schema.Book, db: Session = Depends(get_database_session)):
   bk=model.Books(id=b1.id, title=b1.title, author=b1.author,
publisher=b1.publisher)
   db.add(bk)
   db.commit()
   db.refresh(bk)
   return model.Books(**b1.dict())

@app.get('/list', response_model=List[schema.Book])
def get_books(db: Session = Depends(get_database_session)):
   recs = db.query(model.Books).all()
   return recs

@app.get('/book/{id}', response_model=schema.Book)
def get_book(id:int, db: Session = Depends(get_database_session)):
   return db.query(model.Books).filter(model.Books.id == id).first()

@app.put('/update/{id}', response_model=schema.Book)
def update_book(id:int, book:schema.Book, db: Session = Depends(get_database_session)):
   b1 = db.query(model.Books).filter(model.Books.id == id).first()
   b1.id=book.id
   b1.title=book.title
   b1.author=book.author
   b1.publisher=book.publisher
   db.commit()
   return db.query(model.Books).filter(model.Books.id == id).first()

@app.delete('/delete/{id}')
def del_book(id:int, db: Session = Depends(get_database_session)):
   try:
      db.query(model.Books).filter(model.Books.id == id).delete()
      db.commit()
   except Exception as e:
      raise Exception(e)
   return {"delete status": "success"}