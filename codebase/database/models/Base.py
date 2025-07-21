# from sqlalchemy.orm.decl_api import DeclarativeBase

# class Base(DeclarativeBase):
#     pass

from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
