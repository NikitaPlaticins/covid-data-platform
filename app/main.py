from functools import lru_cache
from pydantic import BaseModel
from fastapi import FastAPI, Query
from app.mongodb import client, annotations
from app.snowflake_db import conn

app = FastAPI()

class Annotation(BaseModel):
    country: str
    state: str
    county: str
    date: str
    comment: str
    author: str
    source: str
    created_at: str

@app.get("/")
def root():
    return {"message": "COVID Platform API is running"}


@app.get("/test")
def test_connections():
    mongo_status = "Connected"
    snowflake_status = "Connected"

    try:
        client.admin.command("ping")
    except Exception as e:
        mongo_status = str(e)

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        version = str(e)

    return {
        "mongodb": mongo_status,
        "snowflake": version
    }

@lru_cache(maxsize=32)
def cached_covid_data(limit: int):
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            DATE,
            STATE,
            COUNTY,
            CASES,
            DEATHS
        FROM NYT_US_COVID19
        LIMIT {limit}
    """)

    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    cursor.close()

    return [dict(zip(columns, row)) for row in rows]

@app.get("/covid")
def get_covid_data(limit: int = Query(10, ge=1, le=100)):
    return cached_covid_data(limit)

    cursor.execute(f"""
        SELECT
            DATE,
            STATE,
            COUNTY,
            CASES,
            DEATHS
        FROM NYT_US_COVID19
        LIMIT {limit}
    """)

    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]

    cursor.close()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return result

@app.get("/annotations")
def get_annotations():
    docs = list(annotations.find({}, {"_id": 0}))
    return docs

@app.post("/annotations")
def add_annotation(annotation: Annotation):
    annotations.insert_one(annotation.dict())
    return {
        "message": "Annotation added successfully"
    }
