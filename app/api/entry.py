from fastapi import APIRouter, Depends, HTTPException, Query
import json
from sqlalchemy.orm import Session
from app.schemas.entry import EntryCreate, EntryOut, PaginatedEntryResponse
from app.models.entry import Entry
from app.core.deps import get_db, get_current_user
from app.core.cache import redis, make_cache_key
from app.models.user import User
from datetime import datetime


router = APIRouter(prefix="/api/v1/entries", tags=["entries"])


@router.get("/search", response_model=list[EntryOut])
async def search_entries(
    q: str = None,
    start_date: str = None,
    end_date: str = None,
    tags: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query_params = {
        "q": q,
        "start_date": start_date,
        "end_date": end_date,
        "tags": tags,
    }
    cache_key = make_cache_key(current_user.id, query_params)

    cached = await redis.get(cache_key)

    if cached:
        return json.loads(cached)

    query = db.query(Entry).filter(Entry.owner_id == current_user.id)

    if q:
        query = query.filter(
            Entry.content.ilike(f"%{q}%") | Entry.title.ilike(f"%{q}%")
        )

    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(Entry.created_at >= start)

    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(Entry.created_at <= end)

    # if tags:
    #     tag_list = [tag.strip() for tag in tags.split(",")]
    #     query = query.join(Entry.tags).filter(Tag.name.in_(tag_list))

    results = query.order_by(Entry.created_at.desc()).all()

    data = [EntryOut.model_validate(r).model_dump() for r in results]

    await redis.set(cache_key, json.dumps(data, default=str), ex=60)

    return data


@router.post("/", response_model=EntryOut)
def create_entry(
    entry: EntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_entry = Entry(**entry.dict(), owner_id=current_user.id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/", response_model=PaginatedEntryResponse)
def list_entries(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    base_query = db.query(Entry).filter(Entry.owner_id == current_user.id)

    total = base_query.count()
    entries = (
        base_query.order_by(Entry.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedEntryResponse(
        total=total,
        page=page,
        page_size=page_size,
        entries=[EntryOut.model_validate(e) for e in entries],
    )


@router.get("/{entry_id}", response_model=EntryOut)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.owner_id == current_user.id)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.owner_id == current_user.id)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": "Deleted successfully"}
