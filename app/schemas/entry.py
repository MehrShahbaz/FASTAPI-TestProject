from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class EntryBase(BaseModel):
    title: str
    content: str


class EntryCreate(EntryBase):
    pass


class EntryOut(EntryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedEntryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    entries: List[EntryOut]
