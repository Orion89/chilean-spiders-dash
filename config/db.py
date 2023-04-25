from sqlalchemy import create_engine
import os

db_uri = os.environ['DB_URI']
engine = create_engine(db_uri)