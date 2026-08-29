from fastapi import FastAPI, UploadFile, File, HTTPException
from app.api.router import api_router
from app.core.database import initialize_database

# CSV Pipeline imports
from app.core.database import check_connection, batches_col, raw_data_col, cleaned_data_col
from app.services.cleaning.pipeline import run_pipeline

initialize_database()

app = FastAPI(
    title="Product Intelligence API",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Product Intelligence API",
        "status": "running"
    }

@app.get("/health")
def health():
    """Confirms the API is up and MongoDB is reachable."""
    # We combine both health checks
    db_status = "ok" if check_connection() else "unreachable"
    return {
        "status": "healthy",
        "mongodb_csv_pipeline": db_status
    }

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