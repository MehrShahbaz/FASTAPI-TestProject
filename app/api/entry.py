from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.entry import EntryCreate, EntryOut
from app.models.entry import Entry
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/entries", tags=["entries"])


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


@router.get("/", response_model=list[EntryOut])
def list_entries(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(Entry)
        .filter(Entry.owner_id == current_user.id)
        .order_by(Entry.created_at.desc())
        .all()
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
