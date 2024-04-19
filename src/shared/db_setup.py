import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import registry as _registry
from sqlalchemy.orm import sessionmaker as _sessionmaker

from shared.settings import POSTGRES_URI

logger = logging.getLogger(__name__)


engine = create_engine(POSTGRES_URI)

sessionmaker = _sessionmaker(bind=engine)

registry = _registry()


def db_health_check():
    try:
        session = sessionmaker()
        session.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except OperationalError as e:
        logger.exception(e)
        raise Exception("connection failed")
