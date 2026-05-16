# SQL AI Agent — Progress Journal

A living document tracking every decision, step, and learning in this project.
Updated after every session.

---

## Project Goal

Build an AI-powered SQL Agent that takes a plain-English question, generates optimized SQL against a real PostgreSQL database, executes it, and returns results. Final deliverable: a live, production-ready app for a hiring manager to interact with.

---

## Key Decisions Made

| Decision | Choice | Reason |
|---|---|---|
| Database | PostgreSQL (local) | Production-realistic, industry standard |
| Dataset | AdventureWorks | Recognized by hiring managers, complex multi-schema structure |
| Local LLM | Ollama — `llama3.2` | Free, runs offline, good SQL generation for its size |
| Cloud LLMs | OpenAI + Anthropic | Added in Phase 2 once local pipeline is proven |
| Python env | `uv` + `SQLAGENT` venv | Fast package management |
| Package install | `uv pip install` | Drop-in for pip, faster |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| Database | PostgreSQL (localhost:5432, db: `Adventureworks`) |
| DB Driver | `psycopg2-binary` + `SQLAlchemy` |
| Local LLM | Ollama (`llama3.2:latest` — 2GB) |
| Cloud LLM (Phase 2) | OpenAI GPT-4o + Anthropic Claude |
| Data | `pandas` |
| Config | `python-dotenv` |
| Frontend (Phase 3) | Streamlit |

---

## Roadmap

### Phase 1 — Foundation (current)
Single script, local LLM, PostgreSQL. Goal: pipeline works end to end.

### Phase 2 — Structure + Multi-Provider
Proper Python package, OpenAI + Claude support, SQL safety guards, self-correction on error.

### Phase 3 — RAG (Retrieval-Augmented Generation)
Instead of passing all 87 tables to the LLM, retrieve only the 3-5 relevant ones per question using ChromaDB vector store. Fixes accuracy and reduces token cost.

### Phase 4 — Production App
Streamlit UI, Docker, deployed to Supabase + Streamlit Cloud. Shareable link for hiring managers.

---

## Session Log

---

### Session 1 — Foundation Setup

**Goal:** Connect to AdventureWorks, explore the schema, build the agent pipeline.

---

#### Step 1 — Install Missing Dependencies

Added three packages to `requirements.txt` that were missing for PostgreSQL connectivity:

```
psycopg2-binary   # PostgreSQL driver
sqlalchemy        # Database ORM / connection management
python-dotenv     # Read .env config files
```

Install command (using uv):
```bash
uv pip install -r requirements.txt --python /path/to/SQLAGENT/bin/python
```

**Key learning:** `pip install` does not update `requirements.txt` automatically. You must add packages manually or run `pip freeze`. We chose manual — keeps the file clean and intentional.

---

#### Step 2 — Configure `.env`

Updated `.env` in the project root with the correct connection string and LLM settings:

```env
DATABASE_URL="postgresql://dhruv@localhost:5432/Adventureworks"
LLM_PROVIDER="ollama"
OLLAMA_MODEL="llama3.2"
```

**Key learning:** Sensitive config (DB credentials, API keys) lives in `.env`, never in code. The `.gitignore` already excludes it. `python-dotenv` loads it at runtime with `load_dotenv()`.

---

#### Step 3 — Database Connection Test (`explore_db.py`)

Wrote a script to verify the PostgreSQL connection and explore AdventureWorks.

**What it does:**
- Connects using `SQLAlchemy` + `create_engine()`
- Queries `information_schema.schemata` for all schemas
- Queries `information_schema.tables` for tables per schema
- Queries `information_schema.columns` for columns per table
- Prints a summary

**Result:**
```
Found 11 schemas: ['hr', 'humanresources', 'pe', 'person', 'pr', 'production', 'pu', 'public', 'purchasing', 'sa', 'sales']
```

6 schemas are empty aliases (hr, pe, pr, pu, sa, public). The 5 real schemas are:

| Schema | Tables |
|---|---|
| humanresources | 6 |
| person | 13 |
| production | 25 |
| purchasing | 5 |
| sales | 19 |

**Key learning:** AdventureWorks uses **schema-qualified table names** (e.g., `sales.salesorderheader`, not just `salesorderheader`). The LLM must always include the schema prefix or the query will fail with "table not found".

---

#### Step 4 — Schema Context Builder (`schema_context.py`)

Wrote a function that fetches the full AdventureWorks schema and formats it as a plain-text string for the LLM prompt.

**What it does:**
- Filters out the 6 empty schemas
- Fetches every table and all its columns from `information_schema.columns`
- Formats each table as:
  ```
  Schema: sales
  Table: salesorderheader
  Columns: salesorderid (integer), orderdate (timestamp), ...
  ```

**Result:**
```
Schemas : ['humanresources', 'person', 'production', 'purchasing', 'sales']
Tables  : 87
Columns : 708
Context length: 25,121 characters (~6,300 tokens)
```

**Key observations:**
- `llama3.2` has a 128K token context window — 6,300 tokens fits easily
- Schema includes **views** (e.g., `vemployee`) — pre-joined tables the LLM can use as shortcuts
- 87 tables × avg 8 columns sent on every query is wasteful but acceptable for Phase 1
- **Phase 3 will fix this with RAG** — only pass the 3-5 relevant tables per question

---

#### Step 5 — Write `agent.py` (in progress)

The core pipeline. Five functions, written by the user.

**Teaching approach for this step:**
- Each function is explained in plain English
- Isolated syntax examples are provided for each piece needed (not the full solution)
- User writes the function themselves and pastes it for review
- Only move to the next function once the current one is confirmed working

| Function | Status | Purpose |
|---|---|---|
| `get_engine()` | Done | Connect to PostgreSQL |
| `build_prompt()` | Done | Combine schema + question into LLM prompt |
| `call_llm()` | Done | Send prompt to Ollama, get response |
| `extract_sql()` | Done | Pull SQL out of LLM response |
| `execute_query()` | Done | Run SQL, return pandas DataFrame |
| `run_agent()` | Done | Orchestrate all five in order |

---

## Files in This Project

| File | Purpose | Status |
|---|---|---|
| `.env` | Config: DB URL, LLM provider, model name | Done |
| `requirements.txt` | All Python dependencies | Done |
| `explore_db.py` | One-time tool: verify DB connection + explore schema | Done |
| `schema_context.py` | Utility: fetch + format schema for LLM | Done |
| `agent.py` | Core agent pipeline | In progress |

---

## Teaching Approach

Every function in this project follows this pattern:

1. **Explain** — what the function does and why it exists
2. **Signature** — the function name, inputs, and what it returns
3. **Syntax examples** — isolated code snippets showing each individual piece needed (not the full answer)
4. **You write it** — combine the pieces into the function yourself
5. **Review** — paste your code, get feedback before moving on

This ensures you understand every line in the project and can explain it to a hiring manager.

---

## Concepts Learned So Far

- **SQLAlchemy `create_engine()`** — creates a reusable DB connection pool from a connection string
- **`information_schema`** — a standard PostgreSQL system schema that describes the database's own structure (schemas, tables, columns)
- **`python-dotenv`** — loads `.env` files into `os.environ` so secrets stay out of code
- **Schema-qualified names** — PostgreSQL requires `schema.tablename` when multiple schemas exist
- **Context window** — the maximum amount of text an LLM can process in one call. `llama3.2` = 128K tokens
- **Why RAG matters** — passing all 87 tables every time is wasteful; RAG will let us retrieve only what's relevant

---

#### Step 5 Result — First Successful Run

```
Question : List all product categories
Generated SQL: SELECT name FROM production.productcategory
Result:
       name
      Bikes
 Components
   Clothing
Accessories
```

**What worked:**
- `llama3.2` correctly schema-qualified the table (`production.productcategory`, not just `productcategory`)
- SQL executed cleanly against PostgreSQL
- Full pipeline ran: schema → prompt → LLM → SQL → result

**Session 1 status: Complete**

---

#### Model Comparison — llama3.2 vs gpt-oss

| Test | llama3.2 (2B) | gpt-oss (13B) |
|---|---|---|
| "List all product categories" | Pass | Pass |
| "Top 5 products by total sales" | Fail — wrong column names, used `TOP` | Pass — correct SQL, correct columns |
| "Which territory had highest revenue" | Fail — mangled table name | Pass — correct JOIN, correct columns |

**Key learning:** Model size matters significantly for complex multi-table queries. llama3.2 hallucinated column names and mangled schema prefixes. gpt-oss read the schema context accurately and generated correct SQL.

**Decision:** Use `gpt-oss` as default local model. Updated `OLLAMA_MODEL=gpt-oss` in `.env`.

---

## Bugs Encountered and Fixed

| Bug | Where | Fix |
|---|---|---|
| Typo `built_prompt` | `build_prompt()` | Renamed to `build_prompt` |
| Schema on same line as heading | `build_prompt()` | Moved `{schema}` to new line |
| `"build_prompt()"` string literal instead of `prompt` variable | `call_llm()` | Changed to `prompt` variable |
| `message` instead of `messages` | `call_llm()` | Fixed parameter name (plural) |
| `import ollama` inside function | `call_llm()` | Moved to top of file |
| `text` variable instead of `llm_response` | `extract_sql()` | Used correct parameter name |
| `call_llm()` called again inside `extract_sql()` | `extract_sql()` | Used `llm_response` parameter directly |
| `print(sql)` before `sql` was defined | `run_agent()` | Moved print after `extract_sql()` call |
| `sys` not imported | top of file | Added `import sys` |

---

*Last updated: Session 1 — Complete*
