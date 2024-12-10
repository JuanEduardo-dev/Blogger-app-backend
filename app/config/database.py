import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Load .env
dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f"No se encontró el archivo .env en: {dotenv_path}")

# URL .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está definida en el archivo .env")

# Create engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # !Conx Pull
    #echo=True  #logs SQL
)

# Class Sesion
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class
Base = declarative_base()

# Depend
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
