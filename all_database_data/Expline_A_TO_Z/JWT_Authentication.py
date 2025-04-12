from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
import traceback
from models.todos import Singup, Post  # Make sure this is your SQLAlchemy model
from config.database import SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Create the database tables
Singup.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for user input
class SingupCreat(BaseModel):
    user_name: str = None
    password: str = None
    email: str = None
    phone_number: str = None
    city: str = None


# Pydantic model for response with ID
class SingupResponse(SingupCreat):
    id: int

    class Config:
        orm_mode = True

@app.post("/singup/", response_model=SingupResponse)
def user_singup(singup: SingupCreat, db: Session = Depends(get_db)):
    try:

        # Create a new user
        db_singup = Singup(
        user_name=singup.user_name,
        password=singup.password,
        email=singup.email, phone_number=singup.phone_number,city=singup.city
    )
        db.add(db_singup)
        db.commit()
        db.refresh(db_singup)
        return db_singup
    except Exception as e:
        return{"error": str(e)}
# ✅ Get all registered users
@app.get("/get_one/{singup_id}", response_model=SingupResponse)
def get_one(singup_id: int, db: Session = Depends(get_db)):
    try:
        singup = db.query(Singup).filter(Singup.id == singup_id).first()  # .first()Returns the first matching record or None if no match is found.find the row where id matches the given singup_id. For getting single table ya db mn say todo table ka data laata hai
        if not singup:
            raise HTTPException(status_code=404, detail="Singup not found")
        return singup  # For returning table
    except Exception as e:
        return {"error": str(e)}
# db mn store all data return krta ahi 
@app.get("/get_alldata", response_model=list[SingupResponse])
def get_all(db: Session = Depends(get_db)):
    try:
        singups = db.query(Singup).all()  # For getting all table ya db mn say todo table ka sara data laata hai
        return singups  # For returning table
    except Exception as e:
        return {"error": str(e)}

# ✅ Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("JWT_Authentication:app", host="127.0.0.1", port=8000, reload=True)

# this command is use for createing and changeing for every table, column, 

# alembic revision --autogenerate -m "create singup table"
# alembic upgrade head
   