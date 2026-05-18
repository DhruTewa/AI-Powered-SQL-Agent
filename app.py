import streamlit as st

# ── Page router ────────────────────────────────────────────────────────────────
# st.navigation() controls the page order in the sidebar.
# Pages are defined here — About first, then Query, then Evaluation.
# Each st.Page() points to a file in pages/ and sets the sidebar label and icon.

about_page    = st.Page("pages/about.py",      title="About",      icon="📖")
query_page    = st.Page("pages/query.py",       title="SQL Agent",  icon="🤖")
eval_page     = st.Page("pages/evaluation.py",  title="Evaluation", icon="📊")

pg = st.navigation([about_page, query_page, eval_page])
pg.run()
