import streamlit as st
from src.components.form import display_form
from src.components.fixed_bottom_bar import display_fixed_bottom_bar
from src.components.navbar import display_navbar
from src.services.ethics_service import ethics_application_function
from src.config import get_openai_api_key
import pandas as pd

def run_app():
    # Get the API key from the config file
    openapi_key = get_openai_api_key()

    # Display the navigation bar
    page = display_navbar()

    # Adjust the main content based on the navigation
    if page == "Home":
        st.title('Welcome to the Ethics Application Generator')
        st.write("Navigate to the Form page to submit your ethics application.")

    elif page == "Form":
        st.title('Ethics Application Generator')

        # Center the main content
        st.markdown(
            """
            <style>
            .main-content {
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }
            .risk-explanation {
                font-size: 18px;
                text-align: left;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="main-content" id="form">', unsafe_allow_html=True)

        # Display the form and get the user inputs
        title, uses_participants, participants_over_18, research_methods = display_form()

        if st.button("Generate Ethics Application"):
            if title and all(research_methods):
                uses_participants_bool = True if uses_participants == "Yes" else False
                participants_over_18_bool = True if participants_over_18 == "Yes" else False

                try:
                    with st.spinner('Generating ethical review...'):
                        response = ethics_application_function(title, uses_participants_bool, participants_over_18_bool, "\n".join(research_methods), openapi_key)

                        # Extracting the risk level and explanation correctly
                        risk_level_info = response['risk_level'].split("\n", 1)

                        risk_level = risk_level_info[0].replace("Risk Level: ", "").strip()
                        risk_explanation = risk_level_info[1].strip() if len(risk_level_info) > 1 else ""

                        # Ensure the risk level is one of the expected values
                        if risk_level not in ["Low", "Medium", "High"]:
                            risk_level = "Unknown"
                            risk_explanation = "The risk level could not be determined."

                        # Store the response in the session state
                        st.session_state['response'] = {
                            "risk": response['risk'],
                            "study_design": response['study_design'],
                            "risk_level": risk_level,
                            "risk_explanation": risk_explanation,
                            "research_methods": research_methods,
                            "ethical_considerations": response['study_design'].split("\n\n")  # Assuming each ethical consideration is separated by two new lines
                        }

                        # Save the result for later review
                        if 'submissions' not in st.session_state:
                            st.session_state['submissions'] = []
                        st.session_state['submissions'].append({
                            "title": title,
                            "risk": response['risk'],
                            "study_design": response['study_design'],
                            "risk_level": risk_level,
                            "research_methods": research_methods,
                            "ethical_considerations": response['study_design'].split("\n\n")  # Assuming each ethical consideration is separated by two new lines
                        })

                    st.success('Ethical review generated successfully!')

                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please enter a research title and describe the research methods.")

        # Display the stored response if available
        if 'response' in st.session_state:
            response = st.session_state['response']
            st.header("Risk Assessment")
            st.write(response['risk'])

            st.header("Study Design")
            st.write(response['study_design'])

            # Display the fixed bottom bar
            display_fixed_bottom_bar(response['risk_level'], response['risk_explanation'])

        st.markdown('</div>', unsafe_allow_html=True)

    # Add a spacer at the bottom for the fixed bar
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
