from typing import Generator
from app.database.main import SessionLocal
def get_db() -> Generator[SessionLocal, None, None]:  # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
