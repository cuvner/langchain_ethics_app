import streamlit as st

def display_fixed_bottom_bar(risk_level, risk_explanation):
    # Determine the color and message based on the risk level
    if "High" in risk_level:
        color = "red"
        message = f"High - <span class='risk-explanation'>{risk_explanation}</span>. Please seek advice from your tutor."
    elif "Medium" in risk_level:
        color = "orange"
        message = f"Medium - <span class='risk-explanation'>{risk_explanation}</span>"
    else:
        color = "green"
        message = f"Low - <span class='risk-explanation'>{risk_explanation}</span>"

    # Display the fixed bottom bar
    st.markdown(
        f"""
        <div class='fixed-bottom-bar' style='background-color:{color};'>
            {message}
        </div>
        <style>
            .fixed-bottom-bar {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                padding: 10px;
                text-align: center;
                font-size: 24px;
                color: white;
                z-index: 1000;
            }}
            .risk-explanation {{
                font-size: 18px;
                text-align: left;
            }}
            body {{
                margin: 0;
                padding: 0;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
