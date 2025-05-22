from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime

class Output(Base):
    __tablename__ = "outputs"

    id = Column(String, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    prompt_id = Column(String, ForeignKey("prompts.id"), nullable=False)
    llm_output = Column(String, nullable=False)
    run_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    time_to_generate = Column(Float, nullable=False)  # Time in seconds

    # Relationships
    video = relationship("Video", back_populates="outputs")
    prompt = relationship("Prompt", back_populates="outputs") 