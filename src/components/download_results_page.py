import streamlit as st
import pandas as pd
# from fpdf import FPDF
# import io

# def create_detailed_dataframe(submissions):
#     # Convert the submissions into a pandas DataFrame for easy handling
#     return pd.DataFrame(submissions)

# def generate_pdf(submissions):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     pdf.set_font('Arial', 'B', 16)
#     pdf.cell(200, 10, txt="Ethical Solutions Results", ln=True, align='C')

#     pdf.set_font('Arial', '', 12)
#     for submission in submissions:
#         pdf.ln(10)  # Add some space between submissions
#         pdf.cell(200, 10, txt=f"Title: {submission['title']}", ln=True)
#         pdf.cell(200, 10, txt=f"Risk: {submission['risk']}", ln=True)
#         pdf.multi_cell(200, 10, txt=f"Study Design: {submission['study_design']}", align='L')
#         pdf.multi_cell(200, 10, txt=f"Ethical Considerations: {'; '.join(submission['ethical_considerations'])}", align='L')

#     # Save PDF to in-memory BytesIO object
#     pdf_output = io.BytesIO()
#     pdf.output(pdf_output)  # Output directly to the in-memory BytesIO object
#     pdf_output.seek(0)  # Go to the start of the file
#     return pdf_output

# def download_results_page():
#     st.title('Download Results')

#     if 'submissions' in st.session_state and st.session_state['submissions']:
#         st.write("Download your ethical solutions results below.")
        
#         # Generate PDF of submissions
#         pdf = generate_pdf(st.session_state['submissions'])
        
#         # Add download button for the PDF
#         st.download_button(
#             label="Download submissions as PDF",
#             data=pdf,
#             file_name='ethical_solutions_results.pdf',
#             mime='application/pdf',
#         )
#     else:
st.write("No submissions available to download.")
