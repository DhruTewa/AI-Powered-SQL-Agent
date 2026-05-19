import streamlit as st
import os
import time
from dotenv import load_dotenv
from core.agent import run_agent
from core.ui import render_header

load_dotenv()

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Agent",
    page_icon="🤖",
    layout="wide"
)

# ── Shared header ──────────────────────────────────────────────────────────────
# Injects global CSS + renders project name and page title consistently
render_header("SQL Agent")
st.caption("Ask questions about the AdventureWorks database in plain English.")
st.divider()

# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "question" not in st.session_state:
    st.session_state.question = ""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    provider = st.selectbox(
        "LLM Provider",
        ["ollama", "openai", "anthropic"],
        help="Select which model to use for SQL generation"
    )

    if provider == "openai":
        st.success("OpenAI (GPT-4o) selected")
    elif provider == "anthropic":
        st.warning("Anthropic API key required")
    else:
        st.info("Ollama runs locally only — not available on the live app")

    st.divider()
    st.markdown("**About this app**")
    st.caption(
        "Converts plain English questions into SQL using "
        "RAG + LLM. Retrieves only relevant tables, "
        "generates SQL, validates it, and returns results."
    )
    st.divider()
    st.caption("**Database:** AdventureWorks")
    st.caption("**Embedding:** text-embedding-3-small (OpenAI)")
    st.caption("**Vector Store:** ChromaDB")

# ── Question input ─────────────────────────────────────────────────────────────
# Larger label rendered via markdown — st.text_input label is too small by default
st.markdown(
    "<p style='font-size:1.2rem; font-weight:600; margin-bottom:6px;'>"
    "Ask a question about your data</p>",
    unsafe_allow_html=True
)

question = st.text_input(
    label="question_input",
    label_visibility="collapsed",     # hides the default label — we use markdown above
    value=st.session_state.question,
    placeholder="e.g. What are the top 5 products by total sales?"
)

# ── Run button ─────────────────────────────────────────────────────────────────
if st.button("Run Query", type="primary", use_container_width=True):

    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        os.environ["LLM_PROVIDER"] = provider

        try:
            start = time.time()

            with st.spinner("Generating SQL and running query..."):
                sql, result = run_agent(question)
                result = result.round(2)

            elapsed = time.time() - start

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Generated SQL")
                st.code(sql, language="sql")

            with col2:
                st.subheader("Results")
                st.dataframe(result, use_container_width=True)

            st.caption(
                f"✓ {len(result)} row(s) · "
                f"{elapsed:.2f}s · "
                f"Provider: {provider}"
            )

            st.session_state.history.insert(0, {
                "question": question,
                "sql": sql,
                "rows": len(result),
                "time": round(elapsed, 2),
                "provider": provider
            })

        except Exception as e:
            st.error(f"Error: {e}")

# ── Query history ──────────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    with st.expander(f"📜 Query History ({len(st.session_state.history)} queries)"):
        for i, item in enumerate(st.session_state.history[:5]):
            st.markdown(f"**{i + 1}. {item['question']}**")
            st.code(item["sql"], language="sql")
            st.caption(
                f"{item['rows']} row(s) · "
                f"{item['time']}s · "
                f"{item['provider']}"
            )
            if i < min(4, len(st.session_state.history) - 1):
                st.divider()
