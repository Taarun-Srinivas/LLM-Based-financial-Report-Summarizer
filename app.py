import streamlit as st
import os
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(text, prompt):
    response = model.generate_content([text, prompt])
    return response.text

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
    for page_num in range(len(pdf_reader.pages)):  # Updated to use len(pdf_reader.pages)
        page = pdf_reader.pages[page_num]  # Updated to use pdf_reader.pages
        text += page.extract_text()
    return text

st.set_page_config(page_title="Financial Document Analyzer")
st.header("Gemini Application")

input_prompt = """
You are an expert in understanding financial documents. We will upload a PDF document. You will have to first generate a rough summary of the document 
and then answer any question based on the content of the document.
"""

uploaded_file = st.file_uploader("Choose a financial document (PDF)", type=["pdf"])

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    summary_prompt = "Generate a rough summary of the following financial document: " + text
    summary = get_gemini_response(text, summary_prompt)
    
    st.subheader("Document Summary")
    st.write(summary)

    # st.write("PDF text extracted successfully.")
    # st.text_area("Extracted Text", text, height=300)

    input = st.text_input("Please ask any questions that you may have: ", key="input")
    submit = st.button("Generate")

    if submit:
        response_prompt = "Answer the following question based on the document summary: " + input
        response = get_gemini_response(summary, response_prompt)
        st.subheader("The response is")
        st.write(response)

    if st.button("Quit"):
        st.write("Thank you for using this app")
