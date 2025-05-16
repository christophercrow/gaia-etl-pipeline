# api/main.py

import os
import psycopg2
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Gaia ETL API")

@app.on_event("startup")
async def startup():
    """
    Establish a PostgreSQL connection when the API starts.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    app.state.dbconn = psycopg2.connect(db_url)
    app.state.dbconn.autocommit = True

@app.on_event("shutdown")
async def shutdown():
    """
    Close the PostgreSQL connection when the API stops.
    """
    if hasattr(app.state, "dbconn"):
        app.state.dbconn.close()

# Include application routes
app.include_router(router)
