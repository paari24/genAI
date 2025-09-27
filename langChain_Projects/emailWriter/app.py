import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["bullet_points"],
    template="""You're an expert email writer. using the following bullet points, create a professional email:  {bullet_points}.
    Provide clear, concise, and well-commented code snippets in your response."""
)

chain = LLMChain(llm=llm, prompt=prompt)

st.title("Smart email Writer")

st.write("Enter key bullet points for the email you want to generate.")

user_input = st.text_area("Enter your key bullet points here:", height =200)

if st.button("Get Code Snippet"):
    if user_input.strip() == "":
        st.warning("Please enter a some bullet points.")
    else:
        with st.spinner("Generating email"):
            response = chain.run(bullet_points=user_input)
            st.write(response, unsafe_allow_html=True)