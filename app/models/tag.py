
# models/tag.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..config.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    description = Column(String, nullable=True)

    publications = relationship(
        "Publication", secondary="publication_tag", back_populates="tags", lazy="joined"
    )
