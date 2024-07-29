import streamlit as st
from src.components.form import display_form
from src.services.ethics_service import ethics_application_function
from src.config import get_openai_api_key
import pandas as pd

def run_app():
    # Get the API key from the config file
    openapi_key = get_openai_api_key()

    st.title('Ethics Application Generator')

    # Display the form and get the user inputs
    title, uses_participants, participants_over_18, research_methods = display_form()

    if st.button("Generate Ethics Application"):
        if title and all(research_methods):
            uses_participants_bool = True if uses_participants == "Yes" else False
            participants_over_18_bool = True if participants_over_18 == "Yes" else False

            try:
                with st.spinner('Generating ethical review...'):
                    response = ethics_application_function(title, uses_participants_bool, participants_over_18_bool, "\n".join(research_methods), openapi_key)
                    risk_level_info = response['risk_level'].split(": ", 1)
                    risk_level = risk_level_info[0]
                    risk_explanation = risk_level_info[1] if len(risk_level_info) > 1 else ""

                st.success('Ethical review generated successfully!')

                st.header("Risk Assessment")
                st.write(response['risk'])

                st.header("Study Design")
                st.write(response['study_design'])

                # Determine the color and message based on the risk level
                if "High" in risk_level:
                    color = "red"
                    message = f"<b style='color:red; font-size:24px;'>High</b> - {risk_explanation}. Please seek advice from your tutor."
                elif "Medium" in risk_level:
                    color = "orange"
                    message = f"<b style='color:orange; font-size:24px;'>Medium</b> - {risk_explanation}"
                else:
                    color = "green"
                    message = f"<b style='color:green; font-size:24px;'>Low</b> - {risk_explanation}"

                # Save the result for later review
                if 'submissions' not in st.session_state:
                    st.session_state['submissions'] = []
                st.session_state['submissions'].append({
                    "title": title,
                    "risk": response['risk'],
                    "study_design": response['study_design'],
                    "risk_level": risk_level
                })

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

                # Display the risk level at the bottom of the page
                st.markdown(f"<div style='position:fixed; bottom:10px; width:100%; text-align:center;'>{message}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a research title and describe the research methods.")
