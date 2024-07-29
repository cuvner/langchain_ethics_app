import streamlit as st

def display_form():
    if 'title' not in st.session_state:
        st.session_state['title'] = ""
    if 'uses_participants' not in st.session_state:
        st.session_state['uses_participants'] = "Yes"
    if 'participants_over_18' not in st.session_state:
        st.session_state['participants_over_18'] = "Yes"
    if 'research_methods' not in st.session_state:
        st.session_state['research_methods'] = [""]

    title = st.text_input("Enter the research title", value=st.session_state['title'], key='title_input')
    uses_participants = st.radio("Does the research use participants?", ("Yes", "No"), index=0 if st.session_state['uses_participants'] == "Yes" else 1)
    participants_over_18 = None
    if uses_participants == "Yes":
        participants_over_18 = st.radio("Are participants over 18?", ("Yes", "No"), index=0 if st.session_state['participants_over_18'] == "Yes" else 1)
    else:
        participants_over_18 = "N/A"

    # Manage dynamic input fields for research methods
    if 'research_methods' not in st.session_state:
        st.session_state.research_methods = ['']

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
    
    st.session_state['title'] = title
    st.session_state['uses_participants'] = uses_participants
    st.session_state['participants_over_18'] = participants_over_18

    return title, uses_participants, participants_over_18, st.session_state.research_methods
