from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas import video as video_schema
from app.services import youtube_service
from app.crud import crud_video

router = APIRouter()

@router.post("/", response_model=video_schema.Video)
def create_video(
    *,
    db: Session = Depends(deps.get_db),
    video_in: video_schema.VideoCreate
) -> video_schema.Video:
    """
    Create new video.
    """
    # Check if video already exists
    video = crud_video.get_by_url(db, url=str(video_in.url))
    if video:
        return video
    
    # Get video metadata from YouTube
    video_metadata = youtube_service.get_video_metadata(str(video_in.url))
    
    # Create video in database
    video = crud_video.create(db, obj_in=video_schema.VideoCreate(
        url=video_in.url,
        title=video_metadata.get("title"),
        channel=video_metadata.get("channel"),
        duration=video_metadata.get("duration"),
        metadata=video_metadata
    ))
    return video

@router.get("/{video_id}", response_model=video_schema.Video)
def get_video(
    *,
    db: Session = Depends(deps.get_db),
    video_id: str
) -> video_schema.Video:
    """
    Get video by ID.
    """
    video = crud_video.get(db, id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.get("/", response_model=List[video_schema.Video])
def get_videos(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> List[video_schema.Video]:
    """
    Get all videos.
    """
    videos = crud_video.get_multi(db, skip=skip, limit=limit)
    return videos 