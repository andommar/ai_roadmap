# IMPORT the Base from our database file, do not recreate it!
from src.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

class ExtractionHistory(Base):
    __tablename__='extraction_history'

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String, nullable=False)
    extracted_email = Column(String, nullable=True)
    # Using timezone.utc is the modern Python standard to avoid server timezone bugs
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

