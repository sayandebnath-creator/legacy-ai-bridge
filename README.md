# Legacy AI Bridge — Natural Language → SQL over Messy Systems

A prototype that simulates how AI can interact with **legacy enterprise systems**.

This project converts natural language queries into SQL and executes them on a **messy, inconsistent database**, then returns a human-readable response.

---

## Why this exists

Modern AI systems assume:
- Clean schemas
- Consistent data
- Well-defined APIs

**Reality in enterprises:**
- Bad column names (`amt_val`, `usr_cd`)
- Inconsistent date formats
- Missing / NULL values
- No proper abstraction layer

This project explores:
> How to bridge AI with "ugly" real-world systems

---

## What it does

**End-to-end pipeline:**
```bash
User Query (Natural Language)
↓
Llama3 (Ollama) → SQL Generation
↓
SQLite (Legacy DB)
↓
Raw Result
↓
Llama3 → Human-readable Answer
```

---

## Simulated Legacy System

The database intentionally includes:

- Poor naming conventions  
- Mixed date formats:
  - `YYYY-MM-DD`
  - `DD/MM/YYYY`
  - `MM-DD-YYYY`
- Missing values
- No schema documentation

### Example Table

```sql
txn_tbl_legacy(
    txn_id INTEGER,
    amt_val FLOAT,
    dt_rec TEXT,
    usr_cd TEXT
)
```

## Example Queries
```bash
total revenue
top users by transaction amount
transactions on 2024-01-10
```

### Example Output
```bash
{
  "question": "total revenue",
  "generated_sql": "SELECT SUM(amt_val) FROM txn_tbl_legacy;",
  "raw_result": [[252534.33]],
  "answer": "The total revenue is $252,534.33."
}
```

## Tech Stack
- Backend: FastAPI
- Database: SQLite (simulated legacy system)
- LLM: Llama3 via Ollama
- Language: Python

## Setup & Run
1. Clone repo
```bash
git clone https://github.com/sayandebnath-creator/legacy-ai-bridge.git
cd legacy-ai-bridge
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install fastapi uvicorn sqlite-utils requests
```

4. Start Ollama (Llama3)
```bash
ollama run llama3
```

- Make sure Ollama is running on:
```bash
http://localhost:11434
```

5. Create the legacy database
```bash
python setup_db.py
```
6. Run the server
```bash
uvicorn main:app --reload
```

- Open:
```bash
http://127.0.0.1:8000/docs
```

## API Usage
### Query endpoint
```bash
GET /query?q=your_question
```
- Example:
```bash
/query?q=total revenue
```

## Known Limitations
This is intentionally not perfect.

- LLM may generate incorrect SQL
- Date filtering is unreliable due to inconsistent formats
- No schema validation layer
- No query safety enforcement (yet)

## Key Insight
The hard problem isn’t generating SQL —
it’s handling inconsistency, ambiguity, and failure in legacy systems.

## Next Improvements
- SQL validation & guardrails (only SELECT allowed)
- Retry mechanism for failed queries
- Schema introspection
- Date normalization layer
- Caching frequent queries

Motivation :-

Inspired by real-world challenges in integrating AI with legacy enterprise infrastructure — where data is messy, undocumented, and inconsistent.