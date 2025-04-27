from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from Pinecone_class import pinecone_ob
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
import time

# Load environment variables
load_dotenv()

# Step 1: Initialize Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")  # Load from .env file for security
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,
    max_output_tokens=1000,
    google_api_key=api_key
)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Step 2: Load PDF
file_path = "Amina Iqbal.pdf"
def get_pdf_text(file_path):
    loader = PyPDFLoader(file_path)
    docs = list(loader.lazy_load())
    return docs

text = get_pdf_text(file_path)
print("✅ PDF loaded successfully")

# Step 3: Split into chunks
def get_text_chunks(text):
    pages = [doc.page_content for doc in text]
    text = " ".join(pages)
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30)
    chunks = splitter.split_text(text)
    return chunks

chunks = get_text_chunks(text)
print("✅ Text chunks created successfully")

# Step 4: Embed chunks
# Ensure chunks are embedded correctly using embeddings
chunk_embeddings = embeddings.embed_documents(chunks)  # Embed the document chunks
print("✅ Chunks embedded successfully")

# Step 5: Create an index and insert data into Pinecone
dimentions = 768  # Set dimension size for the index
index_name = "test-index"
pinecone_ob.create_index(index_name=index_name, dimentions=dimentions)
print("✅ Index created successfully")

# Insert data into Pinecone (use embeddings variable, not chunk_embeddings)
pinecone_ob.insert_data_in_index(documents=chunks, embeddings=chunk_embeddings, index_name=index_name)
print("✅ Data inserted into index successfully")

# Step 6: Retrieve data from Pinecone
# Ensure you're passing the correct arguments
vectordb = pinecone_ob.retrieve_from_index_name(index_name=index_name, embeddings=chunk_embeddings)
print("✅ Data retrieved from index successfully")

# ✅ <class 'langchain.vectorstores.pinecone.Pinecone'>
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Manually embed the query before passing it to retriever
query = "What is the skill of the document?"

# Pass the embedded query to the retriever (retriever expects the embedding, not the raw query)
retrieved_docs = retriever.invoke(query)  # Use the query embedding

print("Retrieved documents:", retrieved_docs)

# template = """Answer the question based only on the following context:

# {context}

# Question: {question}
# """

# prompt = ChatPromptTemplate.from_template(template)
# model = llm

# def format_docs(docs):
#     return "\n\n".join([d.page_content for d in docs])

# # Use the retriever correctly with the chain
# chain = (
#     retriever | format_docs | prompt | model | StrOutputParser()  # Corrected chain flow
# )

# user_input = "Type your question here..."

# # Retrieve documents based on user input
# retrieved_docs = retriever.invoke(user_input)  # Ensure correct query embedding

# # Debugging: print the type and content of retrieved_docs
# st.write(f"retrieved_docs: {retrieved_docs}, type: {type(retrieved_docs)}")

# # Ensure retrieved_docs is a list and properly formatted
# if isinstance(retrieved_docs, list) and retrieved_docs:
#     formatted_docs = format_docs(retrieved_docs)
# else:
#     formatted_docs = "No relevant context found."

# # Debugging: print the type and content of formatted_docs
# st.write(f"formatted_docs: {formatted_docs}, type: {type(formatted_docs)}")
# print("code run")
