# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load DATABASE_URL from environment or default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Load other configuration variables, like THRESHOLD
THRESHOLD = float(os.getenv("THRESHOLD", 0.5))
