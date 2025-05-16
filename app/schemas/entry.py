from pydantic import BaseModel
from datetime import datetime


class EntryBase(BaseModel):
    title: str
    content: str


class EntryCreate(EntryBase):
    pass


class EntryOut(EntryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
