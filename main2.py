from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from models.pdf_info import PDFData
from pydantic import BaseModel
from Pinecone_class import pincoine_ob
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from simple_app.fapiapp import pdf_loader, pdf_splitter, QA_retriever_chain

# Create table if not exists
PDFData.metadata.create_all(bind=engine)

app = FastAPI()

# Initialize embeddings and vector DB
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
name_space = "data"
index_name = "data-index"
dimentions = 1536  # ✅ Fixed spelling mistake (was "dimentions")

api_key = os.getenv("OPENAI_API_KEY")
file_path = r"C:\Users\Amina\Downloads\postgresql\simple_app\amina iqbal.pdf"
try:
    data = pdf_loader(file_path)
    documents = pdf_splitter(data)
except Exception as e:
    raise HTTPException(status_code=500, detail="Error processing PDF: " + str(e))

# Ensure the index exists
pincoine_ob.create_index(index_name=index_name, dimentions=dimentions)
pincoine_ob.insert_data_in_namespace(documents = documents,embeddings = embeddings,index_name = index_name,name_space = name_space)
retriever = pincoine_ob.retrieve_from_namespace(
    index_name=index_name, embeddings=embeddings, name_space=name_space
).as_retriever(search_type="similarity", search_kwargs={"k": 1})

# Initialize LLM globally for efficiency
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db  # ✅ Prevents re-creating session multiple times
    finally:
        db.close()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    """Uploads a PDF, extracts text, splits it, and stores embeddings in Pinecone."""
    if file.filename.split(".")[-1].lower() != "pdf":
        raise HTTPException(status_code=400, detail="File format not supported")

    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    # Process the file
    data = pdf_loader(temp_file_path)
    splited_data = pdf_splitter(data)

    # Insert into vector DB
    pincoine_ob.insert_data_in_namespace(
        documents=splited_data, embeddings=embeddings, index_name=index_name, name_space=name_space
    )

    os.remove(temp_file_path)

    return {"message": "File uploaded and processed successfully"}

@app.post("/retrieve_data/")
async def retrieve_data(question: str):
    """Retrieves relevant data from Pinecone and returns an AI-generated response."""
    try:
        if not retriever:
            return {"message": "No data retrieved from vector DB"}

        responses = QA_retriever_chain(question, retriever)
        return {"response": responses}

    except Exception as e:
        return {"error": f"An error occurred of retriver : {str(e)}"}

# Pydantic model for validation
class PdfInfoBase(BaseModel):
    id : int
    file_id: str
    name: str

    class Config:
        orm_mode = True

@app.post("/create_pdf_info/", response_model=PdfInfoBase)
def create_pdf_info(pdf_data: PdfInfoBase, db: Session = Depends(get_db)):
    """Stores extracted PDF info in PostgreSQL"""
    try:
        new_pdf = PDFData(id= pdf_data.id, file_id=pdf_data.file_id, name=pdf_data.name)
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        return new_pdf
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Proper error handling

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main2:app", host="127.0.0.1", port=8000, reload=True)
# this command is use for createing and changeing for every table, column, 

# alembic revision --autogenerate -m "create pdf_data table"
# alembic upgrade head