
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile # for creating API
from sqlalchemy.orm import Session # ak mrtaba session create hojyga hum bar bar us ka sath kaam krenge
from config.database import SessionLocal, engine # for making connection with database
from models.todos import Todo, Post# for creating table
from pydantic import BaseModel # for validation
from typing import List # for creating list

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
    completed: bool 
    user_id: str
    email: str = None 
    password: str = None


class TodoResponse(TodoCreate):
    id: int

    class Config:
        orm_mode = True

def create_todo(todo: TodoCreate, db: Session = Depends (get_db)) :
    try:
        user = db. query (Users). filter(Users.id = todo.user_id) .first()
        if not user:
            raise HTTPException (status_code=404, detail="User not found" )
        if not user.email == todo.email:
            raise HTTPException(status_code=404, detail="User is not valid")
        if not user_password == todo. password:
            raise HTTPException(status_code=404, detail="User is not valid")
        db_todo = Todo (title=todo.title, description=todo.description,
        completed=todo. completed, user_id=todo.user_id, email=todo.email, password=todo.password) # for creating table
        db.add(db_todo) # for adding data in table

        db.commit() # for committing data in table
        db.refresh(db_todo) # for refreshing data in table 
        return db_todo 
    except Exception as e:
        return {"error": str(e)}
# @app.post("/create_post/")  # For creating API
# def create_post(post: PostCreate, db = Depends(get_db)):  # todocreate for changing details and then chaking and match TODO calass make in todos.py file 
#     try:
#         db_post = Post(id=post.id, hastag=post.hastag, content=post.content)  # For creating table
#         db.add(db_post)  
#         db.commit()  
#         db.refresh(db_post)  
#         return db_post  
#     except Exception as e:
#         return {"error": str(e)}
# @app.get("/get_todos")
# def get_todos(db: Session = Depends(get_db)):
#     try:
#         todos = db.query(Todo).all()  # For getting all table ya db mn say todo table ka sara data laata hai
#         return todos  # For returning table
#     except Exception as e:
#         return {"error": str(e)}
    


# from fastapi import FastAPI, Depends, HTTPException, status
# from pydantic import BaseModel

# app = FastAPI()

# # Mock user data (for demo purposes)
# mock_user_db = {
#     "amina": "password123",
#     "nabiha": "pass456"
# }

# # Request body schema
# class LoginRequest(BaseModel):
#     username: str
#     password: str

# # Authentication logic as a dependency
# def authenticate_user(login: LoginRequest):
#     stored_password = mock_user_db.get(login.username)
#     if not stored_password or stored_password != login.password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password"
#         )
#     return login.username

# # Login endpoint
# @app.post("/login")
# def login(user: str = Depends(authenticate_user)):
#     return {"message": f"Welcome, {user}!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
# this command is use for createing and changeing for every table, column, 

# alembic revision --autogenerate -m "create pdf_data table"
# alembic upgrade head