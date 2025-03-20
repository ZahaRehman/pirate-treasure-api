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

@router.get('/tresure/{id}',status_code=200,response_model=Schemas.ShowQuestions)
def get_Challange(id, db:Session=Depends(get_db)):
    return challanges.show(id, db)

@router.post('/')
def Set_challenge(request : Schemas.setQuestion, db: Session = Depends(get_db)):
    return challanges.set_challenge(request,db)


@router.get("/treasure", status_code=200)
def get_treasure(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return challanges.get_treasure(current_user)