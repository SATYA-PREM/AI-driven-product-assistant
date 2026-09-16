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
from pymongo.errors import PyMongoError
from app.config import settings

try:
    client = MongoClient(
        settings.mongodb_uri,
        connect=False,
        serverSelectionTimeoutMS=4000,
    )
    db = client[settings.database_name]
except Exception as e:
    print(f"Warning: MongoDB client initialization error: {e}")
    client = None
    db = None

class _SafeColProxy:
    """Fallback collection proxy if MongoDB is momentarily unreachable."""
    def __init__(self, col_name):
        self.col_name = col_name

    def __getattr__(self, item):
        if db is not None:
            col = db[self.col_name]
            return getattr(col, item)
        def _dummy(*args, **kwargs):
            return []
        return _dummy

batches_col = db["batches"] if db is not None else _SafeColProxy("batches")
raw_data_col = db["raw_data"] if db is not None else _SafeColProxy("raw_data")
cleaned_data_col = db["cleaned_data"] if db is not None else _SafeColProxy("cleaned_data")
ai_jobs_col = db["ai_jobs"] if db is not None else _SafeColProxy("ai_jobs")
feedback_analyses_col = db["feedback_analyses"] if db is not None else _SafeColProxy("feedback_analyses")


def check_connection() -> bool:
    """Call this once to confirm Mongo is reachable before doing anything else."""
    if client is None:
        return False
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False
