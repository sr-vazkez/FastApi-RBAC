from typing import Generator
from app.database.main import SessionLocal


def get_db() -> Generator[SessionLocal, None, None]:  # type: ignore
    """Obten una session en la BD.

    Yields:
        Generator[SessionLocal, None, None]: Conexion a la BD
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
