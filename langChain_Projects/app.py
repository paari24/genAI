from langchain import OpenAI, PromptTemplate, LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are a helpful assistant. Answer the following question: {user_input}
    Your answer should be concise and informative.
    Your Response:""")

chain = LLMChain(llm=llm, prompt=prompt)

if __name__ == "__main__":
    user_input = input("Please enter your question: ")
    response = chain.run(user_input)
    print("Response:", response)