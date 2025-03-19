
from pydantic import BaseModel
from typing import List,Optional


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode= True



  
class Login(BaseModel):
    username: str
    password: str
    
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    
    
class ShowQuestions(BaseModel):
    island_id: int
    question: str
    
    class Config():
        orm_mode= True
    