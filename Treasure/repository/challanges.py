from sqlalchemy.orm import Session
from .. import models, Schemas
from fastapi import HTTPException,status
from ..hashing import Hash





def show(id:int,db:Session):
    challange= db.query(models.Challenge).filter(models.Challenge.id == id).first()
    if not challange:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"project with the id {id} is not available")
        
    return challange
