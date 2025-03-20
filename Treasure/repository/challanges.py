from sqlalchemy.orm import Session
from .. import models, Schemas
from fastapi import HTTPException,status
from ..hashing import Hash


def show(id: int, db: Session, current_user: Schemas.User):
    active_user = db.query(models.User).filter(models.User.email == current_user.email).first()
    
    if not active_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    user_progress = active_user.progress 
    
    
    if id == 1 or (id == 2 and user_progress.get("island_1")) or (id == 3 and user_progress.get("island_2")):
        challenge = db.query(models.Challenge).filter(models.Challenge.id == id).first()
        
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Challenge with ID {id} not found"
            )
        return challenge
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not unlocked this island yet!"
        )
