import streamlit as st
from dotenv import load_dotenv
import os
import __init__  # Assuming you have the function ethics_application_function in a module named langchain_helper

# Access the API key from Streamlit secrets
openapi_key = st.secrets["OPENAI_API_KEY"]

st.title('Ethics Application Generator')

title = st.text_input("Enter the research title")
uses_participants = st.radio("Does the research use participants?", ("Yes", "No"))
participants_over_18 = st.radio("Are participants over 18?", ("Yes", "No"))
research_methods = st.text_area("Describe the research methods")

if st.button("Generate Ethics Application"):
    if title and research_methods:
        uses_participants_bool = True if uses_participants == "Yes" else False
        participants_over_18_bool = True if participants_over_18 == "Yes" else False
        
        # Ensure that title is passed as a string, uses_participants and participants_over_18 as booleans, and research_methods as a string
        response = __init__.ethics_application_function(title, uses_participants_bool, participants_over_18_bool, research_methods)
        
        st.header("Risk Assessment")
        st.write(response['risk'])
        
        st.header("Study Design")
        st.write(response['study_design'])
    else:
        st.error("Please enter a research title and describe the research methods.")
