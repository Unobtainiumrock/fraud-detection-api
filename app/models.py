from sqlalchemy import Table, Column, Integer, Float, DateTime, func
from app.database import metadata

# Define a table for storing predictions
predictions_table = Table(
    "predictions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("account_id", Integer),
    Column("prediction", Float),
    Column("timestamp", DateTime, default=func.now())
)
