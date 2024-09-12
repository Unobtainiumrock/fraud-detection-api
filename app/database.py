from sqlalchemy import create_engine, MetaData
import databases

from app.config import DATABASE_URL  # Import from config

# Create database instance and metadata
database = databases.Database(DATABASE_URL)
metadata = MetaData()

# Create engine and tables
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
