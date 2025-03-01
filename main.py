from fastapi import FastAPI
from api.routes import auth, lobby
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from database.connection import connect_to_mongo, close_mongo_connection

# Load environment variables
load_dotenv()

# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield  # This allows FastAPI to run the app
    await close_mongo_connection()

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(lobby.router, prefix="/lobby", tags=["Lobby"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
