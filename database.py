from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def session_factory():
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///RPG.db')

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # Create a session
    session = Session()

    return session