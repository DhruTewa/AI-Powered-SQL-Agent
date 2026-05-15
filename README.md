<div align="center">

# AI POWERED SQL Agent

### An LLM-powered autonomous agent that converts natural language into executable SQL

*Ask your database questions in plain English. Get answers as tables.*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat-square&logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-D97757?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Compatible-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## 📋 Overview

**SQL AI Agent** bridges the gap between human language and structured data. Business users, analysts, and engineers often need answers from a database but lack the SQL fluency — or the time — to write queries by hand. This agent removes that bottleneck.

Given a natural-language question such as *"Which products generated the most revenue last quarter?"*, the agent retrieves the relevant schema context via **Retrieval-Augmented Generation (RAG)**, constructs a grounded prompt, invokes a Large Language Model, parses the generated SQL, and executes it against the target database — returning a clean tabular result.

> **Built on three design principles:** *Grounded* (every query is conditioned on the live schema via RAG) · *Composable* (each stage is a pure function, easy to swap or test) · *Provider-agnostic* (works with OpenAI, Anthropic, or any compatible LLM endpoint).

---

## ✨ Key Features

- 🧠 **Natural-language to SQL** — Converts plain English questions into syntactically valid, executable SQL queries
- 🔍 **Schema-aware via RAG** — Uses a vector store to retrieve the most relevant table definitions for each question, dramatically improving accuracy on large schemas
- 🔌 **Multi-provider support** — Drop-in compatibility with OpenAI (GPT-4o) and Anthropic (Claude) APIs
- 🛡️ **Self-validating** — Parses and validates generated SQL before execution; rejects destructive operations under read-only mode
- 🧩 **Composable pipeline** — Each of the five stages is an independently testable pure function
- 🔒 **Safe by default** — Read-only transactions, statement timeouts, connection pooling, and SQL-injection guards
- ⚡ **Production-ready** — Exponential-backoff retries, rate-limit handling, and structured logging built in

---

## 🎬 Demo

```text
> "Top 5 customers by total revenue in Q1 2026"

  Generated SQL:
  SELECT c.customer_name, SUM(o.total_amount) AS revenue
  FROM customers c
  JOIN orders o ON c.id = o.customer_id
  WHERE o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
  GROUP BY c.customer_name
  ORDER BY revenue DESC
  LIMIT 5;

  Result:
  ┌──────────────────┬────────────┐
  │ customer_name    │ revenue    │
  ├──────────────────┼────────────┤
  │ Acme Corp        │ 482,310.00 │
  │ Globex Ltd       │ 391,245.50 │
  │ Initech Inc      │ 287,900.00 │
  │ Umbrella Co      │ 245,180.75 │
  │ Hooli            │ 198,650.25 │
  └──────────────────┴────────────┘
```

---

## 🏗️ Architecture

The agent operates as a **five-stage pipeline**. Each stage transforms its input into a more refined representation, culminating in an executed query and a returned table.

<div align="center">

![SQL AI Agent Architecture](docs/architecture-diagram.svg)

</div>

### Component Breakdown

| # | Component | Function | Responsibility |
|---|-----------|----------|---------------|
| 01 | **Input Processor** | `process_input()` | Normalizes the raw user query; strips whitespace, removes injection-prone characters, detects empty inputs |
| 02 | **Prompt Template** | `build_prompt()` | Combines the question, RAG-retrieved schema context, few-shot examples, and dialect instructions |
| 03 | **API Handler** | `call_llm()` | Sends authenticated `POST` request to the LLM provider; handles retries and rate limits |
| 04 | **SQL Parser** | `parse_sql()` | Extracts and validates the SQL statement; rejects destructive operations under read-only mode |
| 05 | **DB Handler** | `execute_query()` | Executes the query under a read-only transaction; returns results as a pandas DataFrame |

> 📖 See [`docs/technical-reference.html`](docs/technical-reference.html) for full architecture diagrams and component-level documentation.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11+ |
| **Orchestration** | LangChain |
| **LLM Providers** | OpenAI (GPT-4o) · Anthropic (Claude) |
| **Vector Store** | ChromaDB |
| **Embeddings** | OpenAI `text-embedding-3-small` (1536-dim) |
| **Database** | PostgreSQL (via SQLAlchemy) |
| **Data Handling** | pandas · sqlparse |
| **Configuration** | python-dotenv |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- A PostgreSQL database (or any SQLAlchemy-compatible database)
- An API key from OpenAI **and/or** Anthropic

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/sql-ai-agent.git
cd sql-ai-agent
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
# LLM API keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."

# Target database
DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"

# Optional: provider selection & safety
LLM_PROVIDER="anthropic"
READ_ONLY=true
```

**5. Index your database schema**

```bash
python scripts/index_schema.py
```

This embeds your schema once into ChromaDB so the agent can retrieve relevant tables for each query.

---

## 💡 Usage

### CLI

```bash
python -m sql_agent --query "Top 5 customers by revenue last quarter"
```

### Python API

```python
from sql_agent import run_agent

result = run_agent("Show me total sales per region for 2025")
print(result)        # pandas.DataFrame
result.to_csv("sales_report.csv")
```

### Step-by-step pipeline access

```python
from sql_agent import process_input, build_prompt, call_llm, parse_sql, execute_query
from sql_agent.rag import retrieve_schema

query   = process_input("Which products are out of stock?")
context = retrieve_schema(query)
prompt  = build_prompt(query, context)
raw     = call_llm(prompt, provider="anthropic")
sql     = parse_sql(raw)
result  = execute_query(sql)
```

---

## 📁 Project Structure

```
sql-ai-agent/
├── sql_agent/
│   ├── __init__.py
│   ├── agent.py              # Top-level orchestrator (run_agent)
│   ├── input_processor.py    # Stage 01: process_input
│   ├── prompt_builder.py     # Stage 02: build_prompt
│   ├── api_handler.py        # Stage 03: call_llm
│   ├── sql_parser.py         # Stage 04: parse_sql
│   ├── db_handler.py         # Stage 05: execute_query
│   └── rag/
│       ├── vector_store.py   # ChromaDB integration
│       └── retriever.py      # Schema retrieval logic
├── scripts/
│   └── index_schema.py       # One-time schema embedding script
├── tests/
│   └── test_*.py             # Unit tests for each stage
├── docs/
│   ├── architecture-diagram.svg
│   └── technical-reference.html
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📚 API Reference

| Function | Signature | Returns |
|----------|-----------|---------|
| `process_input` | `(query: str) -> str` | Sanitized, normalized query string |
| `build_prompt` | `(query: str, schema_context: str) -> str` | Fully formatted prompt for the LLM |
| `call_llm` | `(prompt: str, provider: str = "anthropic") -> str` | Raw text completion from the model |
| `parse_sql` | `(llm_response: str) -> str` | Validated SQL statement |
| `execute_query` | `(sql: str) -> pd.DataFrame` | Query results as a DataFrame |
| `run_agent` | `(user_query: str) -> pd.DataFrame` | End-to-end pipeline result |

---

## 📊 Benchmarks

Performance evaluated on the [Spider](https://yale-lily.github.io/spider) text-to-SQL benchmark — a cross-domain dataset containing 10,000+ questions across 200 databases.

| Metric | OpenAI (GPT-4o) | Anthropic (Claude) | Notes |
|--------|----------------|-------------------|-------|
| **Execution Accuracy** | `__%` | `__%` | % of queries returning the correct result |
| **Exact Match Accuracy** | `__%` | `__%` | % of queries syntactically identical to gold SQL |
| **Avg. Latency (end-to-end)** | `__ ms` | `__ ms` | Includes RAG retrieval + LLM call + execution |
| **RAG Retrieval Recall@5** | `__%` | `__%` | % of correct tables in top-5 retrieved context |
| **Schemas Tested** | `___` | `___` | Number of distinct database schemas evaluated |

### Test Environment

- **Hardware:** _e.g. M2 MacBook Pro, 16GB RAM_
- **Database:** _e.g. PostgreSQL 15 on local Docker_
- **Embedding Model:** OpenAI `text-embedding-3-small`
- **Sample Size:** _e.g. 1,000 queries from Spider dev set_

> ⚠️ *Numbers above are placeholders. Run `python scripts/run_benchmark.py` to populate with your own evaluation results.*

---

## 🗺️ Roadmap

- [x] Five-stage pipeline with RAG-grounded prompts
- [x] Multi-provider LLM support (OpenAI + Anthropic)
- [x] Read-only safety mode with SQL validation
- [ ] Multi-step reasoning for complex joins (agentic loops)
- [ ] Self-correction loop on execution errors
- [ ] Web UI with chat interface
- [ ] Support for additional dialects (MySQL, BigQuery, Snowflake)
- [ ] Streaming SQL generation
- [ ] Query result visualization

---
