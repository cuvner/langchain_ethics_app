import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd

def display_navbar():
    # Create the navigation bar
    page = st_navbar(["Home", "Form", "Download Submissions"])

    # Handle the "Download Submissions" page
    if page == "Download Submissions":
        if 'submissions' in st.session_state and st.session_state['submissions']:
            df = pd.DataFrame(st.session_state['submissions'])
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
