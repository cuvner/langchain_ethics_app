import streamlit as st
from streamlit_navigation_bar import st_navbar
from src.services.ethical_considerations import create_detailed_dataframe
from src.components.download_results_page import download_results_page  # Adjust this path


def display_navbar():
    # Define the pages and styles for the navigation bar
    pages = ["Home", "Research Methods", "Ethics", "Download Results"]
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
    if page == "Download Results":
        download_results_page()  # Call the download results page function


    return page
