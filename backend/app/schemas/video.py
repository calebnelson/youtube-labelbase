from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
from datetime import datetime

class VideoBase(BaseModel):
    youtube_id: str
    title: str
    description: Optional[str] = None
    video_metadata: Optional[Dict[str, Any]] = None

class VideoCreate(VideoBase):
    pass

class VideoUpdate(VideoBase):
    pass

class VideoInDBBase(VideoBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class Video(VideoInDBBase):
    pass 