from .. import database, Schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status, HTTPException
from ..repository import user
from ..hashing import Hash

get_db = database.get_db


router = APIRouter(
    prefix='/user',
    tags=["user"]
)

@router.post('/',response_model=Schemas.ShowUser)
def create_user(request : Schemas.User, db: Session = Depends(get_db) ):
    return user.create(request,db)
 
 
@router.get('/{id}',response_model=Schemas.ShowUser)
def get_user(id:int ,  db: Session = Depends(get_db) ):
    return user.show(id,db)