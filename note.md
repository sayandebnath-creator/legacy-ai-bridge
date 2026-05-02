# “Legacy → AI Query Bridge”
A service that lets you query messy legacy data using natural language.

# Core Flow:
User → NL query → LLM → SQL → Legacy DB → Result → LLM formats answer

# Architecture
## Components
Fake Legacy DB
- SQLite with ugly schema:
tbl_txn_1998
columns like amt_val, dt_rec, usr_cd
- Backend
Python (FastAPI) or Node (Express)
- LLM Layer
OpenAI OR local (Ollama + Llama3 since you mentioned it earlier)
- Translator
NL → SQL (prompt-based)
- Formatter
SQL result → human-readable answer

# What’s working (this is real signal)
From your output :

- ✅ Correct SQL generation
SELECT SUM(amt_val) → clean, minimal, accurate
- ✅ Query executed successfully
- ✅ LLM formatted answer properly
- ✅ End-to-end pipeline works (NL → SQL → Result → Explanation)