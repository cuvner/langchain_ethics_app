import streamlit as st

def display_form():
    title = st.text_input("Enter the research title")
    uses_participants = st.radio("Does the research use participants?", ("Yes", "No"))
    
    # Conditionally enable or disable the "Are participants over 18?" selection
    participants_over_18 = None
    if uses_participants == "Yes":
        participants_over_18 = st.radio("Are participants over 18?", ("Yes", "No"))
    else:
        st.radio("Are participants over 18?", ("N/A"), disabled=True)
    
    research_methods = st.text_area("Describe the research methods", 
                                    help="Please list the research methods you will use and who they will involve. "
                                         "For example, 'interviews with under 18s', 'surveys with elderly people', etc.")
    return title, uses_participants, participants_over_18, research_methods
