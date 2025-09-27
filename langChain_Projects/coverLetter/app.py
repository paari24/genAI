import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["resume_text","job_title","company_name"],
    template="""you're an expert career coach.
     Using the following resume text: {resume_text} and the job title: {job_title} at {company_name}, create a professional cover letter.    
     Provide clear, concise, and well-commented code snippets in your response."""
)

chain = LLMChain(llm=llm, prompt=prompt)

st.title("Smart Cover Letter Writer")

uploaded_file = st.file_uploader("Upload your resume (PDF format only)", type=["pdf","txt"])
job_title = st.text_input("Enter the job title you are applying for:")
company_name = st.text_input("Enter the company name:")

if st.button("Get Cover Letter"):
    if not uploaded_file and job_title.strip() == "":
        st.warning("Please upload your resume and enter both job title and company name.")
    else:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
        elif uploaded_file.type == "text/plain":
            resume_text = str(uploaded_file.read(), "utf-8")
        else:
            st.error("Unsupported file type. Please upload a PDF or TXT file.")
            resume_text = ""

        if resume_text:
            with st.spinner("Generating cover letter"):
                response = chain.run(resume_text=resume_text, job_title=job_title, company_name=company_name)
                st.write(response, unsafe_allow_html=True)

st.subheader("Note: This app is for educational purposes only. Always review and customize the generated cover letter before using it.")
st.markdown("Developed by [Your Name](https://yourwebsite.com)")