from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./paul_database.db'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:!qazxsw2@localhost/pauldb'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:!qazxsw2@database-1.cova2srjgryp.ap-southeast-1.rds.amazonaws.com/pauldb'

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_sa#me_thread': False})

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
