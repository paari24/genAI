import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["role","job_description"],
    template="""
    Given this Job Role: {role_}
And the Job Description: {job_description_}
Generate 5 **technical** mock interview questions for this role.
Only include questions that test technical skills, knowledge, or problem-solving.
Do NOT include situational or behavioral questions..

For each question, also provide a clear, strong sample answer.

Number them 1 to 5, and format like this:
1.  Question: ...
    Answer:......   
     """
)

chain = LLMChain(llm=llm, prompt=prompt)

st.title("Mock Interview Question Generator")

role = st.text_input("Enter the Job Role (e.g., Software Engineer, Data Scientist):")
job_description = st.text_area("Enter the Job Description:")

if st.button("Generate Questions"):
    if role.strip() == "" or job_description.strip() == "":
        st.warning("Please enter both the Job Role and Job Description.")
    else:
        with st.spinner("Generating questions and answers..."):
            qa_pairs = chain.run(role_=role, job_description_=job_description)
        with st.spinner("Generating email"):
            st.markdown("### Generated Mock Interview Questions and Answers:")
            response = qa_pairs.replace("\n", "<br>")
            st.markdown(response, unsafe_allow_html=True)