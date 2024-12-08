# app/main.py
from fastapi import FastAPI
from app.config.database import get_db
from fastapi.middleware.cors import CORSMiddleware

from .routes import (
    publication_routes,
    user_routes,
    reaction_routes
)

# Create FastAPI app
app = FastAPI(
    title="Proyecto Realidad Nacional",
    description="Backend del aplicativo de realidad nacional",
    version="1.0.0"
)

# CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://propuestas-peru.onrender.com", "http://propuestas-peru.onrender.com"],  # Update with your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(publication_routes.router)
app.include_router(user_routes.router)
app.include_router(reaction_routes.router)