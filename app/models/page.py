# models/page.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..config.database import Base

class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)

    publications = relationship("Publication", back_populates="page", lazy="joined")
