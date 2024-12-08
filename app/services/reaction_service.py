from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.reaction import Reaction
from ..schemas.reaction_schema import ReactionCreate
from datetime import datetime
import uuid

class ReactionService:
    @staticmethod
    def toggle_reaction(db: Session, reaction_data: ReactionCreate):
        """
        Toggle a reaction. If the reaction exists, remove it. 
        If not, add or replace existing reaction.
        """
        existing_reaction = db.query(Reaction).filter(
            and_(
                Reaction.id_user == reaction_data.id_user,
                Reaction.id_publication == reaction_data.id_publication
            )
        ).first()

        if existing_reaction:
            # If same reaction, remove it
            if existing_reaction.type == reaction_data.type:
                db.delete(existing_reaction)
                db.commit()
                return None
            # If different reaction, update
            else:
                existing_reaction.type = reaction_data.type
                existing_reaction.date = datetime.utcnow()
                db.commit()
                return existing_reaction
        
        # Create new reaction
        new_reaction = Reaction(
            id_user=reaction_data.id_user,
            id_publication=reaction_data.id_publication,
            type=reaction_data.type,
            date=datetime.utcnow()
        )
        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)
        return new_reaction
    
    @staticmethod
    def check_user_reaction(db: Session, user_id: uuid.UUID, publication_id: uuid.UUID):
        """
        Check if a user has reacted to a publication.
        Returns a dictionary with:
        - "exists": boolean indicating if the user has reacted.
        - "reaction_type": type of reaction (like or dislike) if exists, otherwise None.
        """
        # Check if there's any reaction from the user on the given publication
        reaction = db.query(Reaction).filter(
            and_(
                Reaction.id_user == user_id,
                Reaction.id_publication == publication_id
            )
        ).first()

        if reaction:
            return {"exists": True, "reaction_type": reaction.type}
        else:
            return {"exists": False, "reaction_type": None}