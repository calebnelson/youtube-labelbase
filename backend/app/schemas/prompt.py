from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class OutputBase(BaseModel):
    llm_output: str
    run_date: datetime
    time_to_generate: float

class Output(OutputBase):
    id: str
    video_id: int
    prompt_id: str

    class Config:
        from_attributes = True

class PromptBase(BaseModel):
    system_prompt: Optional[str] = None
    user_prompt: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(PromptBase):
    pass

class Prompt(PromptBase):
    id: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    outputs: List[Output] = []

    class Config:
        from_attributes = True

# Schema for frontend request
class RunPromptRequest(BaseModel):
    videoUrl: str
    prompt: str
    promptId: str | None = None 