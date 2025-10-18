from contextlib import contextmanager

from src.database.db import session_local


@contextmanager
def get_db():
    """Context manager для работы с сессией"""
    db = session_local()
    try:
        yield db
        db.commit() # автоматический commit при успехе
    except Exception:
        db.rollback() # откат при ошибке
        raise
    finally:
        db.close()
