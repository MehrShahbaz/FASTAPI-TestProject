from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.services.email_summary import send_summary_email

router = APIRouter(prefix="/api/v1/email", tags=["email"])


@router.post("/summary")
async def email_summary(
    backgroud_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    backgroud_tasks.add_task(send_summary_email, current_user, db, 1)
    return {"message": "Summary email will be sent shortly"}
