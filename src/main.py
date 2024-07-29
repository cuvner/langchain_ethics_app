import streamlit as st
from src.components.header import display_header
from src.components.form import display_form
from src.services.ethics_service import ethics_application_function

def main():
    display_header()
    
    title, uses_participants, participants_over_18, research_methods = display_form()
    
    if st.button("Generate Ethics Application"):
        if title and research_methods:
            uses_participants_bool = True if uses_participants == "Yes" else False
            participants_over_18_bool = True if participants_over_18 == "Yes" else False
            
            response = ethics_application_function(title, uses_participants_bool, participants_over_18_bool, research_methods)
            
            st.header("Risk Assessment")
            st.write(response['risk'])
            
            st.header("Study Design")
            st.write(response['study_design'])
        else:
            st.error("Please enter a research title and describe the research methods.")

if __name__ == "__main__":
    main()

