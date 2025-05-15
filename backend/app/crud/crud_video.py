from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.models.video import Video
from app.schemas.video import VideoCreate, VideoUpdate


class CRUDVideo(CRUDBase[Video, VideoCreate, VideoUpdate]):
    def get_by_youtube_id(self, db: Session, *, youtube_id: str) -> Optional[Video]:
        return db.query(Video).filter(Video.youtube_id == youtube_id).first()

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Video]:
        return (
            db.query(Video)
            .filter(Video.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_video = CRUDVideo(Video) 