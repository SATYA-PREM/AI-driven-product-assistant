"""
main.py
---------
The API layer. Thin on purpose -- it just accepts the upload and
calls run_pipeline(), then offers a couple of GET endpoints so you
can look at what landed in each MongoDB collection without needing
to open Atlas.

Run with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs to try it interactively.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from app.database import check_connection, batches_col, raw_data_col, cleaned_data_col
from app.pipeline import run_pipeline

app = FastAPI(title="CSV Validation & Cleaning Pipeline")


@app.get("/health")
def health():
    """Confirms the API is up and MongoDB is reachable."""
    return {"api": "ok", "mongodb": "ok" if check_connection() else "unreachable"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a .csv file. Runs it through the full pipeline:
    parse -> store raw -> validate -> clean -> store cleaned.
    Returns a summary of what happened.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Please upload a .csv file")

    file_bytes = await file.read()
    summary = run_pipeline(filename=file.filename, file_bytes=file_bytes)
    return summary


@app.get("/batches")
def list_batches():
    """Lists every upload batch (the 'receipts'), most recent first."""
    batches = list(batches_col.find().sort("uploaded_at", -1))
    for b in batches:
        b["_id"] = str(b["_id"])
    return batches


@app.get("/batches/{batch_id}/raw")
def get_raw_data(batch_id: str):
    """Returns the untouched raw rows stored for this batch."""
    docs = list(raw_data_col.find({"batch_id": batch_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


@app.get("/batches/{batch_id}/cleaned")
def get_cleaned_data(batch_id: str):
    """Returns the cleaned rows stored for this batch."""
    docs = list(cleaned_data_col.find({"batch_id": batch_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs
