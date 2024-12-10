# models/user.py
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..config.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    mail = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    resetPasswordToken = Column(String, nullable=True)
    resetPasswordExpires = Column(DateTime, nullable=True)
    degreeId = Column(String, ForeignKey("degree.id"), nullable=False)

    publications = relationship("Publication", back_populates="user", lazy="joined", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="user", cascade="all, delete-orphan")