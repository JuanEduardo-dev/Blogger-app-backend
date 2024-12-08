# services/publication_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import UUID, and_

from app.models.reaction import Reaction
from app.schemas.reaction_schema import ReactionType
from ..models.publication import Publication
from ..models.tag import Tag
from ..models.publication_tag import PublicationTag
from ..schemas.publication_schema import PublicationCreate, PublicationUpdate
from datetime import datetime
import uuid

class PublicationService:    
    @staticmethod
    def create_publication(db: Session, publication: PublicationCreate, user_id: uuid.UUID):
        """Create a new publication"""
            # Validate all tags exist
        existing_tags = db.query(Tag.id).filter(Tag.id.in_(publication.tags)).all()
        existing_tag_ids = [tag[0] for tag in existing_tags]
        
        invalid_tags = set(publication.tags) - set(existing_tag_ids)
        if invalid_tags:
            raise ValueError(f"Invalid tags: {invalid_tags}")
        
        db_publication = Publication(
            title=publication.title,
            content=publication.content,
            page_id=publication.page_id,
            user_id=user_id,
            date=datetime.utcnow()
        )
        
        db.add(db_publication)
        db.commit()
        db.refresh(db_publication)

        # Add tags if provided
        if publication.tags:
            for tag_id in publication.tags:
                # First, verify the tag exists
                tag = db.query(Tag).filter(Tag.id == tag_id).first()
                if tag:
                    publication_tag = PublicationTag(
                        publication_id=db_publication.id,
                        tag_id=tag_id
                    )
                    db.add(publication_tag)
            
            db.commit()
            db.refresh(db_publication)

        return db_publication

    @staticmethod
    def update_publication(db: Session, publication_id: uuid.UUID, publication: PublicationUpdate, user_id: uuid.UUID):
        """Update an existing publication, only if the user is the owner"""
        db_publication = db.query(Publication).filter(Publication.id == publication_id).first()
        
        if not db_publication:
            return None
        
        # Verificar si el usuario es el propietario
        if db_publication.user_id != user_id:
            raise ValueError("You are not the owner of this publication")
        
        # Update basic publication details
        db_publication.title = publication.title
        db_publication.content = publication.content

        # Remove existing tags
        db.query(PublicationTag).filter(PublicationTag.publication_id == publication_id).delete()
        
        # Add new tags
        if publication.tags:
            for tag_id in publication.tags:
                publication_tag = PublicationTag(
                    publication_id=publication_id,
                    tag_id=tag_id
                )
                db.add(publication_tag)

        db.commit()
        db.refresh(db_publication)
        return db_publication

    @staticmethod
    def delete_publication(db: Session, publication_id: UUID, user_id: uuid.UUID):
        """Delete a publication, only if the user is the owner"""
        try:
            # First, find the publication
            publication = db.query(Publication).filter(Publication.id == publication_id).first()
            
            if not publication:
                return False
            
            # Verificar si el usuario es el propietario
            if publication.user_id != user_id:
                raise ValueError("You are not the owner of this publication")
            
            # Delete will cascade to publication_tags due to cascade configuration
            db.delete(publication)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error deleting publication: {e}")
            raise

    
    #GET METHODS
    @staticmethod
    def _add_reaction_counts(db: Session, publications):
        """
        Añade likes_count y dislikes_count a una publicación o lista de publicaciones
        """
        # Si se pasa una única publicación, convertirla a lista
        if not isinstance(publications, list):
            publications = [publications]
        
        # Recorrer cada publicación para contar likes y dislikes
        for pub in publications:
            # Contamos los 'likes' y asignamos el valor a 'likes_count'
            pub.likes_count = db.query(Reaction).filter(
                and_(
                    Reaction.id_publication == pub.id,
                    Reaction.type == 'like'
                )
            ).count()
            
            # Contamos los 'dislikes' y asignamos el valor a 'dislikes_count'
            pub.dislikes_count = db.query(Reaction).filter(
                and_(
                    Reaction.id_publication == pub.id,
                    Reaction.type == 'dislike'
                )
            ).count()
        
        # Siempre devolver como lista, incluso si solo hay una publicación
        return publications


    
    @staticmethod
    def get_publications_by_page(db: Session, page_id: int):
        """Get publications for a specific page"""
        publications =  db.query(Publication).filter(Publication.page_id == page_id).all()
        return PublicationService._add_reaction_counts(db, publications)

    @staticmethod
    def get_publications_by_user(db: Session, user_id: uuid.UUID):
        """Get publications for a specific user"""
        publications =  db.query(Publication).filter(Publication.user_id == user_id).all()
        return PublicationService._add_reaction_counts(db, publications)

    @staticmethod
    def get_publications_by_tags(db: Session, tag_ids: List[int]):
        """Get publications that have any of the specified tags"""
        publications =  (
            db.query(Publication)
            .join(PublicationTag)
            .filter(PublicationTag.tag_id.in_(tag_ids))
            .distinct()  # Prevent duplicate publications
            .all()
        )
        return PublicationService._add_reaction_counts(db, publications)

    @staticmethod
    def get_publication_tags(db: Session, publication_id: uuid.UUID):
        """Get tags for a specific publication"""
        publications =  db.query(Tag).join(PublicationTag).filter(PublicationTag.publication_id == publication_id).all()
        return PublicationService._add_reaction_counts(db, publications)
        
    @staticmethod
    def get_publication_by_id(db: Session, publication_id: uuid.UUID):
        """Get the full details of a publication by its UUID"""
        publications =  db.query(Publication).filter(Publication.id == publication_id).first()
        return PublicationService._add_reaction_counts(db, publications)
    
    #USER AND ALL PUBLICATIONS WITH REACTIONS
    
    @staticmethod
    def get_all_publications(db: Session):
        """Get all publications"""
        publications =  db.query(Publication).all()
        return PublicationService._add_reaction_counts(db, publications)
    
    @staticmethod
    def get_user_reactions(db: Session, id_user: uuid.UUID, type: ReactionType = None):
        """Get publications reacted by a user"""
        query = db.query(Publication).join(Reaction).filter(Reaction.id_user == id_user)
        
        if type:
            query = query.filter(Reaction.type == type)
        
        # Obtener todas las publicaciones que ha reaccionado el usuario
        publications = query.all()
        
        # Añadir los contadores de likes y dislikes
        return PublicationService._add_reaction_counts(db, publications)
