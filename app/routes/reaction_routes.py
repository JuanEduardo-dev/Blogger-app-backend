from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..config.database import get_db
from ..services.reaction_service import ReactionService
from ..schemas.reaction_schema import ReactionCreate, PublicationReactionCountResponse
from ..schemas.publication_schema import PublicationResponse

router = APIRouter(prefix="/reactions", tags=["reactions"])

@router.post("/toggle")
def toggle_reaction(
    reaction: ReactionCreate, 
    db: Session = Depends(get_db)
):
    """Toggle a reaction to a publication"""
    try:
        reaction_result = ReactionService.toggle_reaction(db, reaction)
        return {"detail": "Reaction updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reaction-get/{user_id}/{publication_id}", response_model=dict)
def check_user_reaction(
    user_id: uuid.UUID, 
    publication_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """Check if a user has reacted to a publication (like or dislike)"""
    try:
        reaction_info = ReactionService.check_user_reaction(db, user_id, publication_id)
        if reaction_info["exists"]:
            return {"exists": True, "reaction_type": reaction_info["reaction_type"]}
        else:
            return {"exists": False, "reaction_type": reaction_info["reaction_type"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
