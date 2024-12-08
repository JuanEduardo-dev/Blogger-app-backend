from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..config.database import Base

class PublicationTag(Base):
    __tablename__ = "publication_tag"

    publication_id = Column(UUID(as_uuid=True), ForeignKey("publication.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tag.id"), primary_key=True)
