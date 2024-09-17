import streamlit as st
from src.components.form import display_form
from src.components.fixed_bottom_bar import display_fixed_bottom_bar
from src.components.navbar import display_navbar
from src.services.ethics_service import ethics_application_function
from src.config import get_openai_api_key
from src.components.design_methods import design_methods_page
import pandas as pd
import os
import logging

# Function to read the content of homepage.txt using current working directory
def load_homepage_text():
    try:
        # Navigate up one directory level from the current script
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Go up one level
        logging.debug(f"Project root directory: {base_path}")
        
        # Construct the file path relative to the project root
        file_path = os.path.join(base_path, 'forms', 'homepage.txt')
        logging.debug(f"Trying to open file: {file_path}")
        
        # Try to open the file
        with open(file_path, 'r') as file:
            content = file.read()
            logging.info(f"File Content: {content}")  # Log file content
            logging.info("File loaded successfully.")  # Confirm the file was loaded
        return content
    except FileNotFoundError:
        logging.error(f"Error: homepage.txt file not found at: {file_path}")
        return "This AI tool can be used to search the internet for useful advice on choosing appropriate research methods and gauging the ethical implications of these."
    except Exception as e:
        logging.exception(f"An error occurred while loading the file: {e}")
        return ""
    
def run_app():
    # Get the API key from the config file
    openapi_key = get_openai_api_key()

    # Display the navigation bar
    page = display_navbar()

    # Adjust the main content based on the navigation
    if page == "Home":
        st.title('Ethics Application Tool')

        # Load and display the homepage text
        homepage_text = load_homepage_text()
        st.markdown(homepage_text)  # Use st.markdown to preserve line breaks and formatting

    elif page == "Ethics":
        st.title('Explore ethics issues and solutions')

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

        if st.button("Generate Study Design"):
            if title and all(research_methods):
                uses_participants_bool = True if uses_participants == "Yes" else False
                participants_over_18_bool = True if participants_over_18 == "Yes" else False

                try:
                    with st.spinner('Generating study design...'):
                        response = ethics_application_function(title, uses_participants_bool, participants_over_18_bool, "\n".join(research_methods), openapi_key)

                        # Extracting the risk level and explanation correctly
                        risk_level_info = response['risk_level'].split("\n", 1)

                        risk_level = risk_level_info[0].replace("Risk Level: ", "").strip()
                        risk_explanation = risk_level_info[1].strip() if len(risk_level_info) > 1 else ""

                        # Ensure the risk level is one of the expected values
                        if risk_level not in ["Low", "Medium", "High"]:
                            risk_level = "Unknown"
                            risk_explanation = "The risk level could not be determined."

                        # Split study design into ethical considerations
                        ethical_considerations = response['study_design'].split("\n\n")  # Assuming each ethical consideration is separated by two new lines

                        # Store the response in the session state
                        st.session_state['response'] = {
                            "risk": response['risk'],
                            "study_design": response['study_design'],
                            "risk_level": risk_level,
                            "risk_explanation": risk_explanation,
                            "research_methods": research_methods,
                            "ethical_considerations": ethical_considerations
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
                            "ethical_considerations": ethical_considerations
                        })

                    st.success('Study design generated successfully!')

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

    elif page == "Research Methods":
        design_methods_page()

    # Add a spacer at the bottom for the fixed bar
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    run_app()
