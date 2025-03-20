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
        
        
        

def set_challenge(request:Schemas.setQuestion, db: Session):
    new_challenge = models.Challenge(
        island_id = request.island_id,
        question = request.question,
        solution = request.solution
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return new_challenge



def get_treasure(current_user: models.User):
    progress = current_user.progress
    if progress.get("island_1") and progress.get("island_2"):
        return { "message" : "Congratulation! You have found the treasure... It is buried under big W at park"}
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Complete all the islands before accessing treasure"
    )
