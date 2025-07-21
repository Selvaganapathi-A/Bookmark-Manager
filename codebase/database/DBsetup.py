import sqlite3
from pathlib import Path
from typing import Any, Callable, Optional, TypedDict

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.session import Session, sessionmaker


class _Function(TypedDict):
    name: str
    args_count: int
    func: Callable[..., Any]


class Setup:

    def __init__(
        self,
        database: str | Path,
        Base: DeclarativeMeta,
        *,
        echo: bool = True,
        cache: bool = False,
    ):
        self.__engine: Engine
        self.__session: Session
        self.__session_local: sessionmaker[Session]
        self.__base: DeclarativeMeta = Base
        #
        self.__file_db: sqlite3.Connection = sqlite3.connect(
            database,
            cached_statements=200,
            isolation_level='IMMEDIATE',
            autocommit=True,
            check_same_thread=True,
        )
        self.__memory_db: Optional[sqlite3.Connection] = None
        if cache:
            self.__memory_db = sqlite3.connect(
                ':memory:',
                cached_statements=200,
                isolation_level='IMMEDIATE',
                autocommit=True,
                check_same_thread=True,
            )
        self.__engine = create_engine(
            url='sqlite://',
            creator=lambda: self.__memory_db if cache else self.__file_db,
            echo=echo,
        )
        self.__base.metadata.create_all(bind=self.__engine)
        self.__session_local = sessionmaker(bind=self.__engine, autoflush=True)
        self.__session = self.__session_local()

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session_local(self) -> sessionmaker[Session]:
        return self.__session_local

    @property
    def session(self) -> Session:
        return self.__session

    def reset_tables(self):
        self.__base.metadata.drop_all(bind=self.__engine)
        self.__base.metadata.create_all(bind=self.__engine)

    def register_custom_functions(self, *functions: _Function):
        conn = self.__engine.connect().connection
        for func in functions:
            conn.create_function(  # type: ignore
                func['name'], func['args_count'], func['func'])

    def close(self):
        self.__session.commit()
        if self.__memory_db is not None:
            self.__memory_db.backup(self.__file_db)
        self.__engine.dispose()
        self.__memory_db.close() if self.__memory_db is not None else None
        self.__file_db.close()
