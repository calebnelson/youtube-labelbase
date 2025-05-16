from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.api import deps
from app.schemas import prompt as prompt_schema
from app.services import llm_service
from app.crud import crud_prompt, crud_video
from app.services.llm_service import run_prompt
from app.db.models.video import Video
from app.db.models.prompt import Prompt
import uuid

router = APIRouter()

class RunPromptRequest(BaseModel):
    videoUrl: str
    prompt: prompt_schema.PromptCreate

@router.post("/", response_model=prompt_schema.Prompt)
def create_prompt(
    *,
    db: Session = Depends(deps.get_db),
    prompt_in: prompt_schema.PromptCreate
) -> prompt_schema.Prompt:
    """
    Create new prompt and run it against the video.
    """
    # Check if video exists
    video = crud_video.get(db, id=prompt_in.video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Run prompt through LLM
    output = llm_service.run_prompt(
        video_id=prompt_in.video_id,
        system_prompt=prompt_in.system_prompt,
        user_prompt=prompt_in.user_prompt
    )
    
    # Create prompt in database
    prompt = crud_prompt.create(db, obj_in=prompt_schema.PromptCreate(
        video_id=prompt_in.video_id,
        system_prompt=prompt_in.system_prompt,
        user_prompt=prompt_in.user_prompt,
        output=output
    ))
    return prompt

@router.get("/{prompt_id}", response_model=prompt_schema.Prompt)
def get_prompt(
    *,
    db: Session = Depends(deps.get_db),
    prompt_id: str
) -> prompt_schema.Prompt:
    """
    Get prompt by ID.
    """
    prompt = crud_prompt.get(db, id=prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.post("/run_prompt", response_model=Dict[str, Any])
def run_prompt_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    request: prompt_schema.RunPromptRequest
) -> Dict[str, Any]:
  """
  Run a prompt on a video and return the LLM response.
  """
  # Extract YouTube ID from URL
  video_id = request.videoUrl.split("v=")[-1]

  # Create or get video
  video = db.query(Video).filter(Video.youtube_id == video_id).first()
  if not video:
    video = Video(
        youtube_id=video_id,
        title="",  # TODO: Fetch from YouTube API
        description="",  # TODO: Fetch from YouTube API
        video_metadata={},  # TODO: Fetch from YouTube API
        user_id=1  # TODO: Get from authenticated user
    )
    db.add(video)
    db.flush()  # Flush to get the video ID

  # Run the prompt
  output = llm_service.run_prompt(
    video_url=request.videoUrl,
    prompt=request.prompt
  )

  # Create prompt record
  prompt = Prompt(
    id=str(uuid.uuid4()),  # Generate a unique ID
    video_id=video.id,
    system_prompt="",  # TODO: Add system prompt if needed
    user_prompt=request.prompt,
    output=output
  )
  db.add(prompt)
  db.commit()

  return {
    "promptId": prompt.id,
    "output": output
  } 