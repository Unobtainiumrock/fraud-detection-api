from app.database import database
from app.models import predictions_table

# Insert a prediction into the table
async def add_prediction(account_id: int, prediction: float):
    query = predictions_table.insert().values(account_id=account_id, prediction=prediction)
    return await database.execute(query)

# Retrieve predictions from the table
async def get_predictions():
    query = predictions_table.select()
    return await database.fetch_all(query)
