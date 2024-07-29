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
    
    # Manage dynamic input fields for research methods
    if 'research_methods' not in st.session_state:
        st.session_state['research_methods'] = ['']

    def add_method():
        st.session_state.research_methods.append('')

    def remove_method(index):
        st.session_state.research_methods.pop(index)

    st.write("Describe the research methods")
    for i, method in enumerate(st.session_state.research_methods):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.research_methods[i] = st.text_area(f"Method {i+1}", value=method, key=f"method_{i}")
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                remove_method(i)
                st.experimental_rerun()

    if st.button("Add Method"):
        add_method()
        st.experimental_rerun()
    
    return title, uses_participants, participants_over_18, st.session_state.research_methods
