from fastapi import FastAPI
import sqlite3
from llm import generate_sql, format_answer

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/query")
def query(q: str):
    try:
        sql_query = generate_sql(q)

        conn = sqlite3.connect("legacy.db")
        cursor = conn.cursor()

        result = cursor.execute(sql_query).fetchall()

        answer = format_answer(q, result)

        return {
            "question": q,
            "generated_sql": sql_query,
            "raw_result": result,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}