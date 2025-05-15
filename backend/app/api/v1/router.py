from fastapi import APIRouter
from app.api.v1.endpoints import videos, prompts
 
api_router = APIRouter()
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"]) 