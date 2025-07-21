import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from codebase.database.models.Base import Base


@pytest.fixture(scope='session')
def db_engine():
    engine: Engine = create_engine('sqlite:///:memory:', echo=True)
    yield engine
    engine.dispose()


@pytest.fixture(scope='session')
def db_session(db_engine: Engine):
    SessionLocal: sessionmaker[Session] = sessionmaker(bind=db_engine)
    Base.metadata.create_all(bind=db_engine, checkfirst=True)
    session: Session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=db_engine)
