from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from backend.app.api.routes.auth import auth_router
from backend.app.api.routes.recipe import recipe_router

# Initialize the FastAPI app
app = FastAPI(
    title="Cookero Backend API",
    description="The backend API for Cookero",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins in development, should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(recipe_router, tags=["recipes"])

# OAuth2 token URL configuration - ensure this matches the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.get("/")
async def root():
    return {"message": "Welcome to the Cookero API. See /docs for API documentation."}
