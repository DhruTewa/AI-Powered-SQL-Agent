import streamlit as st

PROJECT_NAME = "AI POWERED SQL AGENT"

# Global CSS injected on every page
# Increases base font size by ~4 points and styles the page title consistently
GLOBAL_CSS = """
<style>
    /* Increase base font size across all text elements */
    html, body, [class*="css"] {
        font-size: 18px !important;
    }

    /* Larger, bolder sidebar text */
    .st-emotion-cache-1cypcdb, section[data-testid="stSidebar"] {
        font-size: 17px !important;
    }

    /* Dataframe text */
    .stDataFrame {
        font-size: 17px !important;
    }

    /* Caption text — slightly smaller but still readable */
    .stCaption, small {
        font-size: 15px !important;
    }
</style>
"""


def render_header(page_title: str):
    """
    Call this at the top of every page.
    Injects global CSS and renders the project name + page title consistently.
    """
    # Inject CSS once per page load
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Project name — small, muted, uppercase
    st.markdown(
        f"<p style='font-size:14px; color:grey; margin-bottom:0; "
        f"letter-spacing:2px; text-transform:uppercase;'>{PROJECT_NAME}</p>",
        unsafe_allow_html=True
    )

    # Page title — large, bold, uppercase
    st.markdown(
        f"<h1 style='font-size:2.6rem; font-weight:800; "
        f"text-transform:uppercase; margin-top:0;'>{page_title}</h1>",
        unsafe_allow_html=True
    )
