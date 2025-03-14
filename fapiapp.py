from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from Pinecone_class import pincoine_ob
from langchain_openai import ChatOpenAI
from fastapi import FastAPI, File, UploadFile
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain





app = FastAPI()


def pdf_loader(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()
    # text_data = "\n".join([page.page_content for page in data])
    # return text_data[:5000]  # Limit to 5000 characters
    return data
  


def pdf_splitter(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    splited_pdf = text_splitter.split_documents(data)
    return splited_pdf

# Initialize embeddings and vector DB
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
name_space = "pdf-namespace"
index_name = "pdf-index"
dimentions = 1536
api_key = os.getenv("OPENAI_API_KEY")
# Ensure the index exists
pincoine_ob.create_index(index_name=index_name, dimentions=dimentions)
retriever = pincoine_ob.retrieve_from_namespace(
        index_name=index_name, embeddings=embeddings, name_space=name_space
     ).as_retriever(search_type="similarity", search_kwargs={"k": 1})


# Initialize LLM globally for efficiency
api_key = os.getenv("OPENAI_API_KEY")  # Fetch OpenAI API key
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)  # Initialize only once
def QA_retriever_chain(query, retriever ):
    system_prompt = (
        "Use the given context to answer the question. "
        "If you don't know the answer, say you don't know. "
        "Use and keep the answer concise give only answer do not send page_content. "
        "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    response = chain.invoke({"input": query})
    return response


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File()):
#     """Uploads a PDF, extracts text, splits it, and stores embeddings in Pinecone."""
#     file_extension = file.filename.split(".")[-1].lower()

#     if file_extension != "pdf":
#         raise TypeError("File format not supported")

#     # Save the file temporarily
#     temp_file_path = f"temp_{file.filename}"
#     with open(temp_file_path, "wb") as temp_file:
#         temp_file.write(await file.read())

#     # Process the file
#     data = pdf_loader(temp_file_path)
#     splited_data = pdf_splitter(data)

#     # Insert into vector DB
#     pincoine_ob.insert_data_in_namespace(
#         documents=splited_data, embeddings=embeddings, index_name=index_name, name_space=name_space
#     )

#     # Remove the temporary file
#     os.remove(temp_file_path)

#     return {"message": "File uploaded and processed successfully"}


# @app.post("/retrieve_data/")
# async def retrieve_data(question: str):
#     """Retrieves relevant data from Pinecone and returns an AI-generated response."""
#     try:
#         vector_db = retriever

#         if not vector_db:
#             return {"message": "no data retrieved from vector DB"}

#         responses = QA_retriever_chain(question, retriever)

#         return {"response": responses}

#     except Exception as e:  # Catch any error
#         return {"error": f"An error occurred: {str(e)}"}

 

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("fapiapp:app", host="127.0.0.1", port=8100, reload=True)