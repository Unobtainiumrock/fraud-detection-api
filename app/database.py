from sqlalchemy import create_engine, MetaData
import databases

from app.config import DATABASE_URL

# Define your database URL (you can use PostgreSQL or SQLite)
DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
