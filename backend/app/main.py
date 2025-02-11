from fastapi import FastAPI
from backend.app.api.routes.auth import auth_router

app = FastAPI(title="Cookero Backend API", description="The backend API for Cookero", version="0.1.0")

app.include_router(auth_router, prefix="/auth")