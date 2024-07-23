import streamlit as st
from dotenv import load_dotenv
import os
import __init__  # Assuming you have the function ethics_application_function in a module named langchain_helper

# Access the API key from Streamlit secrets
try:
    openapi_key = st.secrets["openapi_key"]
    if openapi_key:
        print('Got key')

    

except KeyError:
    st.error("The OpenAI API key is not set. Please add your OpenAI API key to the Streamlit secrets.")
    st.stop(openapi_key)

# # Write the result to the Streamlit app
# st.write(
#     "Has environment variables been set:",
#     env_key_set,
# )

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
