import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_sql(question):
    prompt = f"""
        You are working with a legacy database.

        Table: txn_tbl_legacy
        Columns:
        - txn_id (integer)
        - amt_val (transaction amount)
        - dt_rec (date, inconsistent format)
        - usr_cd (user code)

        Rules:
        - Only return valid SQLite SQL
        - No explanation
        - Handle messy date formats carefully

        Question: {question}
        """

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"].strip()


def format_answer(question, result):
    prompt = f"""
        User asked: {question}
        Database result: {result}

        Explain the result in a simple, human-readable way.
        """

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"].strip()