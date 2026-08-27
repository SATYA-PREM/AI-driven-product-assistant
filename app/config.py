"""
config.py
-----------
Loads settings from .env. Read this file first -- it's the simplest
one, and everything else depends on it.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and makes its values available via os.getenv()


class Settings:
    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    database_name: str = os.getenv("DATABASE_NAME", "csv_pipeline_demo")


settings = Settings()

if not settings.mongodb_uri:
    print("WARNING: MONGODB_URI is not set. Copy .env.example to .env and fill it in.")
