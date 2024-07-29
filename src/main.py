import streamlit as st
from src.components.form import display_form
from src.services.ethics_service import ethics_application_function, assess_risk_level
import pandas as pd

def run_app():
    # Access the API key from Streamlit secrets
    try:
        openapi_key = st.secrets["OPENAI_API_KEY"]
    except KeyError:
        st.error("The OpenAI API key is not set. Please add your OpenAI API key to the Streamlit secrets.")
        st.stop()

    st.title('Ethics Application Generator')

    # Display the form and get the user inputs
    title, uses_participants, participants_over_18, research_methods = display_form()

    if st.button("Generate Ethics Application"):
        if title and research_methods:
            uses_participants_bool = True if uses_participants == "Yes" else False
            participants_over_18_bool = True if participants_over_18 == "Yes" else False

            try:
                response = ethics_application_function(title, uses_participants_bool, participants_over_18_bool, research_methods, openapi_key)
                risk_level = assess_risk_level(research_methods, participants_over_18_bool)

                st.header("Risk Assessment")
                st.write(response['risk'])

                st.header("Study Design")
                st.write(response['study_design'])

                st.header("Risk Level")
                st.write(f"The risk level of this study is: {risk_level}")

                # Save the result for later review
                if 'submissions' not in st.session_state:
                    st.session_state['submissions'] = []
                st.session_state['submissions'].append({
                    "title": title,
                    "risk": response['risk'],
                    "study_design": response['study_design'],
                    "risk_level": risk_level
                })

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a research title and describe the research methods.")

    # Add a button to download the submissions as a spreadsheet
    if st.button("Download Submissions as Spreadsheet"):
        if 'submissions' in st.session_state:
            df = pd.DataFrame(st.session_state['submissions'])
            st.download_button(
                label="Download submissions as CSV",
                data=df.to_csv(index=False),
                file_name='submissions.csv',
                mime='text/csv',
            )
        else:
            st.error("No submissions available to download.")
