from fastapi import FastAPI
import sqlite3
from llm import generate_sql, format_answer

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/query")
def is_safe_sql(query: str):
    query = query.lower()
    forbidden = ["drop", "delete", "update", "insert", "alter"]
    return not any(word in query for word in forbidden) and query.strip().startswith("select")

def query(q: str):
    try:
        sql_query = generate_sql(q)

        if not is_safe_sql(sql_query):
            return {"error": "Unsafe query generated"}

        conn = sqlite3.connect("legacy.db")
        cursor = conn.cursor()

        result = cursor.execute(sql_query).fetchall()

        answer = format_answer(q, result)

        return {
            "question": q,
            "generated_sql": sql_query,
            "row_count": len(result),
            "raw_result": result[:5],  # return only first 5 rows for brevity
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}