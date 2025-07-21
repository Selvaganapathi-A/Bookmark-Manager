import m_04_add_urls_bulk
from models import Base
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm.session import Session, sessionmaker


def main():
    session: Session
    engine: Engine = create_engine('sqlite:///sample.db', echo=False)
    #
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #
    sessionLocal = sessionmaker(bind=engine)
    session = sessionLocal()
    #
    m_04_add_urls_bulk.add(session)
    #
    session.commit()
    #
    engine.dispose()


if __name__ == '__main__':
    import os

    # import sql_util
    # [sql_util.get_column_names(table) for table in Base.metadata.sorted_tables]

    os.system('clear')
    main()
