import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.2, model="gpt-4o")

embeddings = OpenAIEmbeddings()

st.title("RAG App: Ask you pdf Anything")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    raw_text = ""

    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text

    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        
    if not raw_text.strip():
        st.error("No text found in the uploaded PDF.")

    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(raw_text)

        if not chunks:
            st.error("Text splitting resulted in no chunks.")
        else:
            st.success(f"PDF processed successfully! Number of text chunks created: {len(chunks)}")

            vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

            qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(),
            )
    
    user_question = st.text_input("Ask a question about the PDF:")

    if user_question:
                with st.spinner("Generating answer..."):
                    response = qa.run(user_question)
                    st.write("Answer:")
                    st.write(response)