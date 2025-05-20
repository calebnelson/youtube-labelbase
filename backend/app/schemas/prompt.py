from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# Schema for database model
class PromptBase(BaseModel):
    video_id: int
    user_id: Optional[int] = None
    system_prompt: Optional[str] = None
    user_prompt: str
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