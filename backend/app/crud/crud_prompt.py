from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.models.prompt import Prompt
from app.schemas.prompt import PromptCreate, PromptUpdate


class CRUDPrompt(CRUDBase[Prompt, PromptCreate, PromptUpdate]):
    def get_multi_by_video(
        self, db: Session, *, video_id: int, skip: int = 0, limit: int = 100
    ) -> List[Prompt]:
        return (
            db.query(Prompt)
            .filter(Prompt.video_id == video_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_prompt = CRUDPrompt(Prompt) 