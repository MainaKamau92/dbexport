from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# an Engine, which the Session will use for connection
DB_URL = os.getenv("DB_URL")
# resources
some_engine = create_engine(DB_URL)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

# work with sess

# myobject = MyObject("foo", "bar")
# session.add(myobject)
# session.commit()
