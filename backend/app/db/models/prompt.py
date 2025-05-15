from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class Prompt(Base):
    id = Column(String, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("video.id"))
    system_prompt = Column(String)
    user_prompt = Column(String)
    output = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 