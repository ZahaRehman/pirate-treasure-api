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
