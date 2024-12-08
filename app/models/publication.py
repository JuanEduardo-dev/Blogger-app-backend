# models/publication.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..config.database import Base

class Publication(Base):
    __tablename__ = "publication"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    page_id = Column(Integer, ForeignKey("page.id"), nullable=False)

    user = relationship("User", back_populates="publications", lazy="joined")
    page = relationship("Page", back_populates="publications", lazy="joined")
    tags = relationship(
        "Tag", secondary="publication_tag", back_populates="publications", lazy="joined", 
    )
    reactions = relationship("Reaction", back_populates="publication", cascade="all, delete-orphan")