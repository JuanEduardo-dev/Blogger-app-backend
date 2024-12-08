from sqlalchemy import Column, Integer, String
from ..config.database import Base

class Degree(Base):
    __tablename__ = "degree"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
