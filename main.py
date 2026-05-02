from fastapi import FastAPI
import sqlite3
from llm import generate_sql, format_answer

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

def is_safe_sql(query: str):
    query = query.lower()
    forbidden = ["drop", "delete", "update", "insert", "alter"]
    return not any(word in query for word in forbidden) and query.strip().startswith("select")

@app.get("/query")
def query(q: str):
    try:
        sql_query = generate_sql(q)

        if not is_safe_sql(sql_query):
            return {"error": "Unsafe query generated"}

        conn = sqlite3.connect("legacy.db")
        cursor = conn.cursor()
        try :
            result = cursor.execute(sql_query).fetchall()
        except sqlite3.Error:
            # Retry once with correction prompt
            sql_query = generate_sql(q + " (fix the SQL, previous query failed)")

            if not is_safe_sql(sql_query):
                return {"error": "Unsafe query generated (retry)"}

            result = cursor.execute(sql_query).fetchall()
        finally:
            conn.close()
        
        if not result:
            answer = "No data found for this query."
        else:
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