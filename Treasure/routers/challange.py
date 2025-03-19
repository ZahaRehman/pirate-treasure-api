from .. import database, Schemas, models, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status, HTTPException
from ..repository import challanges
from typing import List
from ..hashing import Hash
from ..database import get_db 
from ..oauth2 import get_current_user



router =APIRouter(
    tags=['/challange']
)

@router.get('/island/{id}',response_model=Schemas.ShowQuestions)
def show(id : int , db: Session = Depends(get_db)):
    return challanges.show(id, db)