from app.db.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.entry import Entry
from app.core.security import hash_password
from datetime import datetime, timezone

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Entry).delete()
db.query(User).delete()
db.commit()

user1 = User(email="alice@example.com", hashed_password=hash_password("password123"))
user2 = User(email="bob@example.com", hashed_password=hash_password("password456"))
db.add_all([user1, user2])
db.commit()
