import streamlit as st
from streamlit_navigation_bar import st_navbar
from src.services.ethical_considerations import create_detailed_dataframe

def display_navbar():
    # Define the pages and styles for the navigation bar
    pages = ["Home", "Research Methods", "Ethics", "Download Submissions"]
    styles = {
        "nav": {
            "background-color": "rgb(123, 209, 146)",
        },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }

    # Create the navigation bar
    page = st_navbar(pages, styles=styles)

    # Handle the "Download Submissions" page
    if page == "Download Submissions":
        if 'submissions' in st.session_state and st.session_state['submissions']:
            df = create_detailed_dataframe(st.session_state['submissions'])
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download submissions as CSV",
                data=csv,
                file_name='submissions.csv',
                mime='text/csv',
            )
        else:
            st.write("No submissions available to download.")

    return page
