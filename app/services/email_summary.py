from fastapi_mail import MessageSchema
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.entry import Entry

from app.core.email_config import fast_mail


def generate_summary(entries: list[Entry]) -> str:
    if not entries:
        return "<p>You have no journal entries in this perios</p>"

    lines = f"<h3>{len(entries)} entries from your DevLog:</h3><ul>"

    for e in entries:
        lines += f"<li><strong>{e.title}</strong> ({e.mood}) — {e.created_at.strftime('%Y-%m-%d')}</li>"

    lines += "</ul>"
    return lines


async def send_summary_email(user: User, db: Session, days: int = 1):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    entries = (
        db.query(Entry)
        .filter(Entry.owner_id == user.id, Entry.created_at >= cutoff)
        .order_by(Entry.created_at.desc())
        .all()
    )

    if not entries:
        return

    html = generate_summary(entries)

    message = MessageSchema(
        subject="Your DevLog Summary",
        recipients=[user.email],
        body=html,
        subtype="html",
    )

    await fast_mail.send_message(message)
