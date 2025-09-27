import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import requests
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
# =====API KEYS=====
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

client = OpenAI()

#===== Load PDF & Create Index =====
@st.cache_resource
def load_pdfs_and_create_index(pdf_paths):
     docs = []
     for path in pdf_paths:
          reader = PdfReader(path)
          text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
          docs.append(text)
          
          chunks = []
          for doc in docs:
                for i in range(0, len(doc), 500):
                       chunk = doc[i:i + 500]
                       if chunk.strip():
                              chunks.append(chunk)

                model = SentenceTransformer('all-MiniLM-L6-v2')
                vectors = model.encode(chunks)
                
                index = FAISS.IndexFlatL2(vectors.shape[1])
                index.add(vectors)
                
                return index, chunks, model
          
#===== Retrieve Relevant Chunks =====
def retrieve(query, index, chunks, model, top_k=3):
     query_vector = model.encode([query])
     distances, indices = index.search(query_vector, top_k)
     return [chunks[i] for i in indices[0] ]

#===== Verifier =====
def is_answer_correct(answer, query):
     prompt = f"""
     Question: {query}
     Answer: {answer}  

        Is the answer correct? Respond with 'yes' or 'no'.
        """
     response = client.chat.completions.create(model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that verifies answers."},
                {"role": "user", "content": prompt}],            temperature=0)
     return response.choices[0].message.content

#===== Fall Back : Web Search =====
def web_search(query):
     search_url = "https://serpapi.com/search.json"
     params = {
          "engine": "google",
          "q": query,
          "api_key": serpapi_api_key
     }
     response = requests.get(search_url, params=params)
     results = response.json()
     organic = results.get("organic_results", [])
     snippets = []
     for result in organic:
          snippet = result.get("snippet") or result.get("title")
          if snippet:
               snippets.append(snippet)
               if snippets:
                     return "\n".join(snippets) 
               else:
                     # if search failed , ask llm to answer from scratch
                     fallback_prompt = f"""
                     The web search for the question "{query}" returned no results. 
                     Please answer the question based on your knowledge."""
                     
                     response = client.chat.completions.create(model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that answers questions."},
                                {"role": "user", "content": fallback_prompt}], temperature=0)
                     return response.choices[0].message.content
               

#===== Orchestrator =====
def answer_query(query, index, chunks, model):
     relevant_chunks = retrieve(query, index, chunks, model)
     context = "\n".join(relevant_chunks)
     
     verdict = is_answer_correct(context, query)
     
     if verdict.strip().lower() == 'yes':
          return f"Based on the document context:\n{context}    \nThe answer to your question '{query}' is correct."
     else:
          serp_reults = web_search(query)
          return f"Based on the web search results:\n{serp_reults}    \nThe answer to your question '{query}' is provided from web search."
     
#===== Streamlit UI =====
st.title("Agentic RAG: PDF + Web Search")
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
if uploaded_files:
     pdf_paths = [file for file in uploaded_files]
     index, chunks, model = load_pdfs_and_create_index(pdf_paths)
     
     user_question = st.text_input("Ask a question about the PDFs:")
     
     if user_question:
          with st.spinner("Generating answer..."):
               response = answer_query(user_question, index, chunks, model)
               st.write("Answer:")
               st.write(response)