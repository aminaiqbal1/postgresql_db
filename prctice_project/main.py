
# use FOR one table 
from models.tabels import Post
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from config.database import get_db, engine
Post.metadata.create_all(bind=engine)


app = FastAPI()

class PostCreate(BaseModel):
    
    tittle: str = None
    name: str = None
class PostResponse(PostCreate):
    id: int
    class Config:
        orm_mode = True
# class PostResponse(BaseModel):
#     id: int
#     name: str
#     tittle: str

#     class Config:
#         orm_mode = True
@app.post("/posts/")
def create_post(chack: PostCreate, db: Session = Depends(get_db)):
    try:
        db_post = Post(tittle=chack.tittle, name=chack.name )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return {"data" :db_post,
                "message": "Post created successfully",
                "status": True}
    except Exception as e:
        return {"message": "Post not created",
                "status": False,
                "error": str(e)}


# Read All Users
@app.get("/posts/")
def get_posts( db= Depends(get_db)):
    return db.query(Post).all()
# Read User by ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db= Depends(get_db)):
    return db.query(Post).filter(Post.id == user_id).first()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
# this command is use for createing and changeing for every table, column, 

# alembic revision --autogenerate -m "create users table"
# alembic upgrade head
