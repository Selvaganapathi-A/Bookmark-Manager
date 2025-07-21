import m_01_dump
import m_02_dump
import m_03_icon
from models import Base
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm.session import Session, sessionmaker


def main():
    session: Session
    engine: Engine = create_engine('sqlite:///sample.db', echo=False)
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #
    sessionLocal = sessionmaker(bind=engine)
    session = sessionLocal()
    #
    m_02_dump.dump(session)
    #
    # m_03_icon.write_icons_to_file(session=session)
    #
    session.commit()
    #
    engine.dispose()


if __name__ == '__main__':
    import os

    os.system('clear')
    main()
