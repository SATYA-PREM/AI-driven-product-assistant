"""
database.py
-------------
Connects to MongoDB and defines THREE collections (MongoDB's word for
"folder" -- a named bucket of documents):

    batches       -- one document per CSV upload (like a receipt: filename,
                      when it was uploaded, how many rows, current stage)
    raw_data       -- one document per ORIGINAL row from the CSV, untouched.
                      Every row here has a batch_id linking it back to its
                      upload, so you can always find "every row from upload X".
    cleaned_data    -- one document per row that PASSED validation and was
                      cleaned. Also tagged with batch_id, plus a link back
                      to its raw_data document via raw_id.

Why two separate collections instead of one? Two reasons a beginner
should know:
  1. You always want an untouched copy of what was originally uploaded,
     in case your cleaning logic has a bug and you need to reprocess.
  2. Bad/invalid rows get dropped during cleaning -- so raw_data and
     cleaned_data will have DIFFERENT numbers of documents. Keeping
     them separate makes that difference visible and queryable.
"""

from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.mongodb_uri)
db = client[settings.database_name]

# These lines are where the collections get created.
# MongoDB creates a collection automatically the first time you
# insert into it -- you don't need to set these up manually in Atlas.
batches_col = db["batches"]
raw_data_col = db["raw_data"]
cleaned_data_col = db["cleaned_data"]

# Milestone 2 Collections
ai_jobs_col = db["ai_jobs"]
feedback_analyses_col = db["feedback_analyses"]


def check_connection() -> bool:
    """Call this once to confirm Mongo is reachable before doing anything else."""
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False
