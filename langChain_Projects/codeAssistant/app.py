import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["code_task"],
    template="""You're a professional coding assistant. Help the user with the following task:  {code_task}.
    Provide clear, concise, and well-commented code snippets in your response."""
)

chain = LLMChain(llm=llm, prompt=prompt)

st.title("Code Assistant")

st.write("Describe your coding task, and I'll help you with code snippets!")

user_input = st.text_area("Enter your coding task here:")

if st.button("Get Code Snippet"):
    if user_input.strip() == "":
        st.warning("Please enter a coding task.")
    else:
        with st.spinner("Generating code snippet..."):
            response = chain.run(code_task=user_input)
            st.code(response, language='python')