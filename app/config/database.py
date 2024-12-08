import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Cargar el archivo .env (asegúrate de que exista)
dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f"No se encontró el archivo .env en: {dotenv_path}")

# URL de conexión a la base de datos desde el .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está definida en el archivo .env")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Sin conexión pool
    echo=True  # Habilitar logs SQL
)

# Crear una clase de sesión configurada
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para modelos declarativos
Base = declarative_base()

# Dependencia para la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
