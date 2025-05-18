from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.mood import Mood


class EntryBase(BaseModel):
    title: str
    content: str


class EntryCreate(EntryBase):
    pass


class EntryOut(EntryBase):
    id: int
    created_at: datetime
    mood: Optional[Mood] = None

    model_config = {"from_attributes": True}


class PaginatedEntryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    entries: List[EntryOut]
