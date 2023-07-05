from pydantic import BaseModel
class Book(BaseModel):
   id: int
   title: str
   author:str
   publisher: str
   class Config:
      orm_mode = True
