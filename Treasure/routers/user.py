from .. import database, Schemas, models,oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status, HTTPException
from ..repository import user
from ..hashing import Hash
from ..database import get_db 
from ..oauth2 import get_current_user

get_db = database.get_db


router = APIRouter(
    prefix='/user',
    tags=["user"]
)

@router.post('/',response_model=Schemas.ShowUser)
def create_user(request : Schemas.User, db: Session = Depends(get_db),get_current_user: Schemas.User= Depends(oauth2.get_current_user) ):
    return user.create(request,db)
 
 
@router.get('/{id}',response_model=Schemas.ShowUser)
def get_user(id:int ,  db: Session = Depends(get_db) ):
    return user.show(id,db)