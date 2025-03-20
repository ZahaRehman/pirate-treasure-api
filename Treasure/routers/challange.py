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
def get_Question_by_Island(id:int , db:Session=Depends(get_db), current_user: Schemas.User=Depends(get_current_user)):
    return challanges.show(id, db, current_user)


@router.post("/{id}/submit")
def submit_answer(
    id: int, 
    answer: str, 
    db: Session = Depends(get_db), 
    current_user: Schemas.User = Depends(get_current_user)
):
    active_user_query = db.query(models.User).filter(models.User.email == current_user.email)
    active_user = active_user_query.first()
    
    if not active_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    challenge = db.query(models.Challenge).filter(models.Challenge.id == id).first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge with ID {id} not found"
        )
    
    user_progress = active_user.progress or {"island_1": False, "island_2": False, "treasure": False}

    if id == 2 and not user_progress.get("island_1"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must complete Island 1 first!"
        )
    elif id == 3 and not user_progress.get("island_2"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must complete Island 2 first!"
        )
    
    if answer.strip().lower() == challenge.solution.strip().lower():
        if id == 1:
            user_progress["island_1"] = True
        elif id == 2:
            user_progress["island_2"] = True
        elif id == 3:
            user_progress["treasure"] = True

        active_user_query.update({"progress": user_progress})
        db.commit()
        
        updated_user = active_user_query.first()
        return {"message": "Correct answer! You have unlocked the next island."}
    
    else:
        return {"message": "Wrong answer! Try again."}
