import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the versioned API router (all endpoints are attached there)
from app.api.v1.router import api_router

# Main FastAPI application object
app = FastAPI(
    title="M3M Chatbot Backend API",
    version="1.0.0",
    description="Clean API backend for chatbot; frontend connects via HTTP endpoints.",
)

# CORS middleware allows your separate frontend app to call this backend.
# Keep this list explicit for security; add production frontend URL later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # CRA dev server
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all version-1 routes under /api/v1
# Example: POST /api/v1/chat
app.include_router(api_router, prefix="/api/v1")

# Run the app
port = int(os.environ.get("PORT", 8000))
uvicorn.run("api_main:app", host="0.0.0.0", port=port)
