from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM

from ..config.database import Base

class Reaction(Base):
    __tablename__ = 'reactions'
    
    id_user = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)  # Cambié 'users.id' a 'user.id'
    id_publication = Column(UUID(as_uuid=True), ForeignKey('publication.id'), primary_key=True)
    date = Column(DateTime(timezone=True), nullable=False)
    type = Column(ENUM('like', 'dislike', name='type_reaction'), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="reactions")
    publication = relationship("Publication", back_populates="reactions")