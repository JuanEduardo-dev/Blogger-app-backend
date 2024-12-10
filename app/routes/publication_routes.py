# routes/publication_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.schemas.reaction_schema import ReactionType

from ..config.database import get_db
from ..services.publication_service import PublicationService
from ..schemas.publication_schema import PublicationCreate, PublicationUpdate, PublicationResponse, TagSchema

router = APIRouter(prefix="/publications", tags=["publications"])

@router.post("/", response_model=PublicationResponse)
def create_publication(
    publication: PublicationCreate, 
    db: Session = Depends(get_db)
):
    """Create a new publication"""
    try:
        db_publication = PublicationService.create_publication(db, publication, publication.user_id)
        return db_publication
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{publication_id}/{user_id}", response_model=PublicationResponse)
def update_publication(
    publication_id: uuid.UUID, 
    user_id: uuid.UUID,
    publication: PublicationUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing publication, only if the user is the owner"""
    try:
        db_publication = PublicationService.update_publication(
            db, publication_id, publication, user_id
        )
        if not db_publication:
            raise HTTPException(status_code=404, detail="Publication not found")
        return db_publication
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.delete("/{publication_id}/{user_id}")
def delete_publication(
    publication_id: uuid.UUID, 
    user_id: uuid.UUID,  # Post by path
    db: Session = Depends(get_db)
):
    """Delete a publication, only if the user is the owner"""
    try:
        success = PublicationService.delete_publication(db, publication_id, user_id)  # Pasamos el user_id
        if not success:
            raise HTTPException(status_code=404, detail="Publication not found")
        return {"detail": "Publication deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
@router.get("/all-items", response_model=List[PublicationResponse])
def get_all_publications(db: Session = Depends(get_db)):
    """Get all publications."""
    db_publications = PublicationService.get_all_publications(db)
    if not db_publications:
        raise HTTPException(status_code=200, detail="No publications found")
    return db_publications

@router.get("/user-reactions/{user_id}/likes", response_model=List[PublicationResponse])
def get_user_liked_publications(
    user_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """Get publications liked by a user"""
    return PublicationService.get_user_reactions(db, user_id, ReactionType.LIKE)

@router.get("/user-reactions/{user_id}/dislikes", response_model=List[PublicationResponse])
def get_user_disliked_publications(
    user_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """Get publications disliked by a user"""
    return PublicationService.get_user_reactions(db, user_id, ReactionType.DISLIKE)

@router.get("/by-page/{page_id}", response_model=List[PublicationResponse])
def get_publications_by_page(
    page_id: int, 
    #skip: int = 0, 
    #limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Get publications for a specific page"""
    return PublicationService.get_publications_by_page(db, page_id)

@router.get("/by-user/{user_id}", response_model=List[PublicationResponse])
def get_publications_by_user(
    user_id: uuid.UUID, 
    #skip: int = 0, 
    #limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Get publications for a specific user"""
    return PublicationService.get_publications_by_user(db, user_id)

@router.get("/by-tags", response_model=List[PublicationResponse])
def get_publications_by_tags(
    tag_ids: List[int] = Query(..., min_items=1),
    #skip: int = 0, 
    #limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Obtener publicaciones con las etiquetas especificadas"""
    return PublicationService.get_publications_by_tags(db, tag_ids)

@router.get("/{publication_id}/tags", response_model=List[TagSchema])
def get_publication_tags(
    publication_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """Get tags for a specific publication"""
    return PublicationService.get_publication_tags(db, publication_id)

@router.get("/{publication_id}", response_model=PublicationResponse)
def get_publication_by_id(
    publication_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """Get a publication by its ID"""
    publication = PublicationService.get_publication_by_id(db, publication_id)
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication