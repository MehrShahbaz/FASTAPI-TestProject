from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware  # ✅ ADD THIS

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.core.rate_limiter import limiter
from app.api import auth, entry, email

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)


@app.get("/api/v1/healthcheck")
def healthcheck():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(entry.router)
app.include_router(email.router)
