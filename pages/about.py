import streamlit as st
from core.ui import render_header

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="About — AI SQL Agent",
    page_icon="📖",
    layout="wide"
)

# ── Shared header ──────────────────────────────────────────────────────────────
render_header("About")
st.caption("Built with Python · LangChain-free RAG · Ollama · ChromaDB · PostgreSQL")
st.divider()

# ── Overview ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("What is this?")
    st.markdown("""
This application is an **AI-powered SQL Agent** that bridges the gap between
plain English and structured databases.

Instead of writing SQL manually, you type a business question — the agent
figures out which tables are relevant, generates the correct SQL query,
validates it for safety, executes it, and returns the results as a clean table.

Built on the **AdventureWorks** database — an industry-standard sample dataset
covering sales, products, employees, customers and purchasing across 87 tables
and 5 schemas.
    """)

with col2:
    # Key stats displayed as metrics
    st.metric("Database Tables", "87")
    st.metric("Schemas", "5")
    st.metric("LLM Providers", "3")
    st.metric("RAG Retrieval", "Top 8 tables")

st.divider()

# ── How it works ───────────────────────────────────────────────────────────────
st.subheader("How It Works")
st.markdown("""
The agent runs a **five-stage pipeline** on every question:
""")

# Pipeline displayed as numbered columns
stages = st.columns(5)
pipeline = [
    ("1️⃣", "Schema Retrieval",
     "ChromaDB finds the 8 most relevant tables for your question using vector similarity"),
    ("2️⃣", "Prompt Building",
     "The question + relevant schema are combined into a structured prompt for the LLM"),
    ("3️⃣", "SQL Generation",
     "The LLM generates a PostgreSQL query grounded in the actual schema"),
    ("4️⃣", "Validation",
     "The SQL is checked for dangerous keywords and confirmed to be a SELECT statement"),
    ("5️⃣", "Execution",
     "The validated SQL runs against AdventureWorks and results are returned as a table"),
]

for col, (icon, title, desc) in zip(stages, pipeline):
    with col:
        st.markdown(f"### {icon}")
        st.markdown(f"**{title}**")
        st.caption(desc)

st.divider()

# ── RAG explained ──────────────────────────────────────────────────────────────
st.subheader("What is RAG?")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
**Retrieval-Augmented Generation (RAG)** solves a core problem with LLMs and databases:

AdventureWorks has 87 tables. Sending all of them to the LLM on every question
is wasteful and reduces accuracy — the model has to sift through irrelevant
tables to find the ones it needs.

**RAG fixes this in two phases:**

**Indexing** *(done once, upfront)*
Each table description is converted into a vector (a list of numbers that
represents its meaning) and stored in ChromaDB.

**Retrieval** *(done per query)*
Your question is also converted into a vector. ChromaDB finds the tables whose
vectors are closest to your question — only those 8 tables are sent to the LLM.
    """)

with col2:
    st.markdown("**Without RAG**")
    st.code("""
Prompt size:  ~25,000 characters
Tables sent:  87 (all of them)
LLM accuracy: Lower — too much noise
Token cost:   High on every query
    """)

    st.markdown("**With RAG**")
    st.code("""
Prompt size:  ~3,000 characters
Tables sent:  8 (most relevant only)
LLM accuracy: Higher — focused context
Token cost:   ~85% reduction
    """)

st.divider()

# ── Tech stack ─────────────────────────────────────────────────────────────────
st.subheader("Tech Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Core**")
    st.markdown("""
- Python 3.12
- PostgreSQL (AdventureWorks)
- SQLAlchemy + psycopg2
- pandas
    """)

with col2:
    st.markdown("**AI / LLM**")
    st.markdown("""
- Ollama (local LLM + embeddings)
- OpenAI GPT-4o *(API key required)*
- Anthropic Claude *(API key required)*
- ChromaDB (vector store)
    """)

with col3:
    st.markdown("**App**")
    st.markdown("""
- Streamlit (UI)
- python-dotenv (config)
- uv (package management)
    """)

st.divider()

# ── How to use ─────────────────────────────────────────────────────────────────
st.subheader("How to Use")

st.markdown("""
1. **Select a provider** from the sidebar — start with *Ollama* (no API key needed)
2. **Type a question** in plain English, or click one of the example buttons
3. **Click Run Query** — the agent retrieves relevant tables, generates SQL, and runs it
4. **View results** — the generated SQL and result table appear side by side
5. **Compare models** — visit the Evaluation page to benchmark multiple providers on the same questions
""")

st.info(
    "💡 **Tip:** For best results, ask specific business questions. "
    "Example: *'Which sales territory had the highest revenue last year?'* "
    "works better than *'show me sales'*."
)

st.divider()

# ── Safety ─────────────────────────────────────────────────────────────────────
st.subheader("Safety")
st.markdown("""
The agent is **read-only by design**. Every generated SQL query passes through
a validator before execution:

- Queries containing `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE` or `ALTER` are rejected immediately
- Queries that don't start with `SELECT` or `WITH` are rejected
- All queries run in a standard read transaction — no writes can occur
""")

st.divider()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.caption("Built by Dhruv Tewari · AI-Powered SQL Agent · AdventureWorks Database")
