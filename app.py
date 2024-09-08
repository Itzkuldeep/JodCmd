from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
import fitz
import google.generativeai as genai

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf(uplded_file):
    if uplded_file is not None:
        pdf_doc = fitz.open(stream= uplded_file.read(), filetype="pdf")
        # page = pdf_content[0]
        # text = page.get_text()
        # return text
        first_page  = pdf_doc.load_page(0) # extracting first page  

        # conversion of page to img
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes()

        # encoded to base64
        pdf_parts = [
            {"mime_type":"image/jpeg",
             "data":base64.b64encode(img_byte_arr).decode()}
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")
    
# UI
st.set_page_config(page_title="JodCMD")
st.header("JobCMD")
input_text = st.text_area("Job Description:", key="input")
uplded_file = st.file_uploader("Upload Resume in PDF format:", type=["pdf"])


if uplded_file is not None:
    st.write("PDF uploaded Successfully")

submit1 = st.button("Tell me about the Resume")
submit2 = st.button("Percentage Match")

input_prompt_l ="""You are an experienced HR with Tech Experience in the filed of any one job role from Data science, 
Full Stack, Web Devlopment, Big Data Engineer, DevOps, Data Analyst. Your Task is to review the provided resume against
the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile align with the highlights the strength and weakness
of the applicant in relation to the specified job role """

input_prompt_2 ="""You are an experienced HR with Tech Experience in the filed of any one job role from Data science, 
Full Stack, Web Devlopment, Big Data Engineer, DevOps, Data Analyst. Your Task is to review the provided resume against
the job description for these profiles.
Give me the percentage match if the resume matches the Job Description.
First the output should come as percentage, then keywords missing and last final.
"""

if submit1:
    if uplded_file is not None:
        pdf_content = input_pdf(uplded_file)
        response = get_gemini_response(input_prompt_l, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the PDF file")

if submit2:
    if uplded_file is not None:
        pdf_content = input_pdf(uplded_file)
        response = get_gemini_response(input_prompt_2, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the PDF file")