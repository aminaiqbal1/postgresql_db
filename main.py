
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile # for creating API
from sqlalchemy.orm import Session # ak mrtaba session create hojyga hum bar bar us ka sath kaam krenge
from config.database import SessionLocal, engine # for making connection with database
from models.todos import Todo, Post# for creating table
from pydantic import BaseModel # for validation
from typing import List # for creating list

# 1️⃣ PostgreSQL & Why It’s Used
# PostgreSQL (also known as Postgres) is a relational database.
# It stores structured data in tables with columns and rows.
# It supports ACID (Atomicity, Consistency, Isolation, Durability), making it reliable for transactions.
# ✅ FastAPI uses PostgreSQL for structured storage
# ✅ Pinecone is used for vector storage (semantic search)
# ✅ PostgreSQL is used for structured data (metadata, user data, etc.)
Todo.metadata.create_all(bind=engine) # ya alumbic ki trhn he kaam krta hai mgr s mn verson create n hoty hain
# for creating table in database
app = FastAPI() # for creating API
def get_db():
    db = SessionLocal() # for making connection with database
    try:
        yield db # for creating session
    finally:
        db.close() # for closing session
# pydantic model for validation and serialization
class TodoCreate(BaseModel): # for creating table
    title: str 
    description: str  = None
    gmail: str = None 

class PostCreate(BaseModel): # for creating table
    id: int = None
    hastag: str = None
    content: str = None

class TodoResponse(TodoCreate):
    id: int

    class Config:
        orm_mode = True

@app.post("/todos/", response_model=TodoResponse)  # For creating API
def create_todo(todo: TodoCreate, db = Depends(get_db)):  # todocreate for changing details and then chaking and match TODO calass make in todos.py file 
    try:
        db_todo = Todo(title=todo.title, description=todo.description,gmail = todo.gmail)  # For creating table
        db.add(db_todo)  # For adding table
        db.commit()  # For committing table
        db.refresh(db_todo)  # For refreshing table
        return db_todo  # For returning table
    except Exception as e:
        return {"error": str(e)}
@app.post("/create_post/")  # For creating API
def create_post(post: PostCreate, db = Depends(get_db)):  # todocreate for changing details and then chaking and match TODO calass make in todos.py file 
    try:
        db_post = Post(id=post.id, hastag=post.hastag, content=post.content)  # For creating table
        db.add(db_post)  # For adding table
        db.commit()  # For committing table
        db.refresh(db_post)  # For refreshing table
        return db_post  # For returning table
    except Exception as e:
        return {"error": str(e)}
@app.get("/get_todos")
def get_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todo).all()  # For getting all table
        return todos  # For returning table
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
# this command is use for createing and changeing for every table, column, 

# alembic revision --autogenerate -m "create pdf_data table"
# alembic upgrade head