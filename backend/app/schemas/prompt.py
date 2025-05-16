from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# Schema for database model
class PromptBase(BaseModel):
    video_id: str
    prompt: str
    output: Optional[Dict[str, Any]] = None

class PromptCreate(PromptBase):
    pass

class PromptUpdate(PromptBase):
    pass

class PromptInDBBase(PromptBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Prompt(PromptInDBBase):
    pass

# Schema for frontend request
class RunPromptRequest(BaseModel):
    videoUrl: str
    prompt: str 