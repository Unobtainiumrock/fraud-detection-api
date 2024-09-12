# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Load threshold from environment variable or default to 0.5
THRESHOLD = float(os.getenv("THRESHOLD", 0.5))
