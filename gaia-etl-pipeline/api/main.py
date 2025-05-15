#api/main.py
import os
import psycopg2
from fastapi import FastAPI
from api.routes import router

app = FastAPI()

@app.on_event("startup")
async def startup():
    db_url = os.getenv("DATABASE_URL")
    app.state.dbconn = psycopg2.connect(db_url)
    app.state.dbconn.autocommit = True

@app.on_event("shutdown")
async def shutdown():
    app.state.dbconn.close()

app.include_router(router)
