from fastapi import FastAPI

from app.api.router import api_router

# main.py

from app.core.database import initialize_database

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

    return {
        "status": "healthy"
    }