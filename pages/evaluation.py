import streamlit as st
import os
import time
import pandas as pd
from core.agent import run_agent
from core.ui import render_header, ollama_available

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Model Evaluation",
    page_icon="📊",
    layout="wide"
)

# ── Shared header ──────────────────────────────────────────────────────────────
render_header("Model Evaluation")
st.caption("Compare SQL generation quality across LLM providers.")
st.divider()

# ── Golden dataset ─────────────────────────────────────────────────────────────
# These 10 questions cover different SQL complexity levels:
# simple lookups, aggregations, joins, date filters, CTEs
TEST_QUESTIONS = [
    "List all product categories",
    "How many employees are in each department?",
    "What are the top 5 products by total sales amount?",
    "Which sales territory had the highest revenue?",
    "What is the average order value by customer type?",
    "Show total sales amount by product category",
    "Who are the top 3 sales representatives by total revenue?",
    "Which products have a list price above the average list price?",
    "Show total number of orders placed each year",
    "Which sales territories had total revenue above the company-wide average?",
]

# ── Provider registry ──────────────────────────────────────────────────────────
# available=False means API key not yet configured — checkbox will be disabled
PROVIDERS = {
    "ollama":    {"label": "Ollama (local)",     "available": ollama_available()},
    "openai":    {"label": "OpenAI (gpt-4o)",    "available": True},
    "anthropic": {"label": "Anthropic (Claude)", "available": False},
}

# ── Model selector ─────────────────────────────────────────────────────────────
st.subheader("1. Select Models to Compare")
cols = st.columns(len(PROVIDERS))
selected_providers = []

for i, (key, info) in enumerate(PROVIDERS.items()):
    with cols[i]:
        if info["available"]:
            # Ollama is checked by default since it's available locally
            checked = st.checkbox(info["label"], value=(key == "ollama"))
            if checked:
                selected_providers.append(key)
        else:
            # Disabled checkbox with explanation
            st.checkbox(info["label"], value=False, disabled=True)
            st.caption("⚠️ Coming soon")

# ── Question selector ──────────────────────────────────────────────────────────
st.subheader("2. Select Test Questions")

# Allow the user to run all or a subset — defaults to first 5 for speed
selected_questions = st.multiselect(
    "Choose questions (default: first 5)",
    options=TEST_QUESTIONS,
    default=TEST_QUESTIONS[:5]
)

st.caption(
    f"{len(selected_providers)} model(s) × "
    f"{len(selected_questions)} question(s) = "
    f"{len(selected_providers) * len(selected_questions)} total runs"
)

# ── Run evaluation ─────────────────────────────────────────────────────────────
if st.button("▶ Run Evaluation", type="primary", use_container_width=True):

    if not selected_providers:
        st.warning("Select at least one model to evaluate.")
    elif not selected_questions:
        st.warning("Select at least one question.")
    else:
        results = []
        total_runs = len(selected_providers) * len(selected_questions)
        progress_bar = st.progress(0, text="Starting evaluation...")
        count = 0

        for provider in selected_providers:
            # Switch the active provider before each batch of questions
            os.environ["LLM_PROVIDER"] = provider

            for question in selected_questions:
                progress_bar.progress(
                    count / total_runs,
                    text=f"[{provider}] {question[:60]}..."
                )

                try:
                    start = time.time()
                    sql, df = run_agent(question)
                    elapsed = round(time.time() - start, 2)

                    results.append({
                        "Provider":   provider,
                        "Question":   question,
                        "Status":     "✓ Pass",
                        "Rows":       len(df),
                        "Time (s)":   elapsed,
                        "SQL":        sql
                    })

                except Exception as e:
                    results.append({
                        "Provider":   provider,
                        "Question":   question,
                        "Status":     "✗ Fail",
                        "Rows":       0,
                        "Time (s)":   0,
                        "SQL":        str(e)
                    })

                count += 1

        progress_bar.progress(1.0, text="Evaluation complete")

        # ── Summary metrics ────────────────────────────────────────────────────
        st.divider()
        st.subheader("Summary")

        df_results = pd.DataFrame(results)
        summary_cols = st.columns(len(selected_providers))

        for i, provider in enumerate(selected_providers):
            provider_df = df_results[df_results["Provider"] == provider]
            pass_count  = len(provider_df[provider_df["Status"] == "✓ Pass"])
            total_q     = len(provider_df)
            passed_df   = provider_df[provider_df["Status"] == "✓ Pass"]
            avg_time    = passed_df["Time (s)"].mean() if not passed_df.empty else 0

            with summary_cols[i]:
                # st.metric shows a prominent number with a label
                st.metric(
                    label=PROVIDERS[provider]["label"],
                    value=f"{pass_count}/{total_q} passed",
                    delta=f"Avg {avg_time:.1f}s" if pass_count > 0 else "No passes"
                )

        # ── Comparison table (pivot: questions as rows, providers as columns) ────
        st.subheader("Comparison Table")

        # Build one column per provider showing "✓ 2.1s  5 rows" or "✗ Error"
        pivot_data = {"Question": selected_questions}
        for provider in selected_providers:
            label = PROVIDERS[provider]["label"]
            col_values = []
            for question in selected_questions:
                match = df_results[
                    (df_results["Provider"] == provider) &
                    (df_results["Question"] == question)
                ]
                if not match.empty:
                    row = match.iloc[0]
                    if row["Status"] == "✓ Pass":
                        col_values.append(f"✓  {row['Time (s)']}s  {int(row['Rows'])} rows")
                    else:
                        col_values.append("✗  Failed")
                else:
                    col_values.append("—")
            pivot_data[label] = col_values

        pivot_df = pd.DataFrame(pivot_data).set_index("Question")

        # Colour cells: green for pass, red for fail
        def highlight_cells(val):
            if str(val).startswith("✓"):
                return "background-color: #d4edda; color: #155724; font-weight: bold"
            elif str(val).startswith("✗"):
                return "background-color: #f8d7da; color: #721c24; font-weight: bold"
            return ""

        styled = pivot_df.style.map(highlight_cells)
        st.dataframe(styled, width='stretch')

        # ── Summary row beneath the table ──────────────────────────────────────
        summary_data = {"Metric": ["Execution Rate", "Avg Latency (passed only)"]}
        for provider in selected_providers:
            label = PROVIDERS[provider]["label"]
            provider_df = df_results[df_results["Provider"] == provider]
            pass_count = len(provider_df[provider_df["Status"] == "✓ Pass"])
            total_q    = len(provider_df)
            passed_df  = provider_df[provider_df["Status"] == "✓ Pass"]
            avg_time   = passed_df["Time (s)"].mean() if not passed_df.empty else 0
            summary_data[label] = [
                f"{pass_count}/{total_q}  ({int(pass_count/total_q*100)}%)" if total_q > 0 else "—",
                f"{avg_time:.1f}s" if pass_count > 0 else "—"
            ]

        st.dataframe(
            pd.DataFrame(summary_data).set_index("Metric"),
            width='stretch'
        )

        # ── Generated SQL viewer ───────────────────────────────────────────────
        with st.expander("🔍 View Generated SQL for Each Run"):
            for _, row in df_results.iterrows():
                st.markdown(
                    f"**{row['Provider']} — {row['Question']}** "
                    f"({row['Status']})"
                )
                st.code(row["SQL"], language="sql")
                st.divider()
