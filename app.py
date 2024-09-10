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
    
def extract_keywords(job_desc, resume_text):
        
    """Extract keywords that are common in both job description and resume text."""
    if not job_desc or not resume_text:
        st.warning("Job description or resume text is missing.")
        return None

    # Convert to lowercase for comparison
    job_desc_lower = job_desc.lower()
    resume_text_lower = resume_text.lower()

    # Extract keywords
    keywords = set(job_desc_lower.split()) & set(resume_text_lower.split())
    return ', '.join(keywords)  

# Function to extract and summarize PDF content
def extract_pdf_text(uplded_file):
    """Extract text from a multi-page PDF and handle edge cases."""
    if uplded_file is not None:
        try:
            # Check if the file is not empty
            if uplded_file.size == 0:
                raise ValueError("The uploaded PDF file is empty. Please upload a valid PDF.")

            pdf_doc = fitz.open(stream=uplded_file.read(), filetype="pdf")
            text = ""

            # Extract text from all pages
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc.load_page(page_num)
                page_text = page.get_text("text")

                if page_text.strip():  # Only add non-empty pages
                    text += page_text + "\n\n"
                else:
                    st.warning(f"Page {page_num+1} is empty or contains no extractable text.")

            if not text.strip():
                raise ValueError("The PDF contains no extractable text.")

            # Summarize if text is too long
            if len(text) > 5000:
                st.warning("The PDF is large, showing the first 5000 characters as a summary.")
                text = text[:5000] + "...\n\n[Content Truncated]"

            return text

        except fitz.EmptyFileError:
            st.error("The uploaded PDF file is corrupted. Please upload a valid file.")
            return None
        except Exception as e:
            st.error(f"An error occurred while reading the PDF: {str(e)}")
            return None
    else:
        st.warning("No file uploaded.")
        return None

# UI
st.set_page_config(page_title="JodCMD", layout="wide")
st.header("JobCMD")
input_text = st.text_area("Job Description:", key="input")
uplded_file = st.file_uploader("Upload Resume in PDF format:", type=["pdf"])


if uplded_file is not None:
    st.write("PDF uploaded Successfully")


# Buttons for different actions
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    submit1 = st.button("Tell me about the Resume")
with col2:
    submit2 = st.button("Percentage Match")
with col3:
    submit3 = st.button("Extract Skills")


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

input_prompt_3 = """You are an experienced HR professional with a background in technical roles such as Data Science, Full Stack Development, Web Development, Big Data Engineering, DevOps, or Data Analysis. 
Your task is to carefully analyze the provided resume and extract key technical skills, tools, programming languages, and relevant job-specific keywords that align with any of the mentioned roles. 
Focus on identifying the most critical terms that match the expected job profile requirements."""

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

if submit3 and uplded_file:
    pdf_content = input_pdf(uplded_file)
    matched_keywords = extract_keywords(input_prompt_3, pdf_conent,input_text)
    st.subheader("Matched Skills/Keywords:")
    st.write(matched_keywords)
elif submit3:
    st.warning("Please upload the PDF file.")