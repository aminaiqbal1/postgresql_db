from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Singup(Base):
    __tablename__ = "singup"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)




















    
# # # Relationship with Post
# class Post(Base):
#     __tablename__ = 'post'

#     id = Column(Integer, primary_key=True, index=True)  # Primary key for unique identification
#     hastag = Column(String, nullable=False)  # Cannot be empty
#     content = Column(String, nullable=False)  # Cannot be empty

#     # Define relationship with Todo 
#     todo = relationship("Todo", back_populates="post")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)  # Primary key for unique identification
    name = Column(String, nullable=False)  # Cannot be empty
# Relationship with Todo
# class Todo(Base):
#     __tablename__ = 'todo'

#     id = Column(Integer, primary_key=True, index=True)  # Use:Marks the column as a primary key.Benefit:Uniquely identifies each row.Ensures no duplicates.Primary key for unique identification
#     title = Column(String, nullable=False)  
#     description = Column(String, nullable=True)  
#     gmail = Column(String, unique = True)  
#     completed = Column(Integer, default=0)  

#     # Foreign key for posts table with ondelete post tbale ki id ko todo table mn daalna ka lia
#     # ondelete = "CASCADE" means if post is deleted then todo will also be deleted
#     post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
#     post = relationship("Post", back_populates="todo")
#     user = relationship("Todo", back_populates="post")


#  # relationship with post table ya do table ka doran relationship bnata hai 
#     # s ko ab hum alumbic .env file mn base model ko import krynga 
# # alembic revision --autogenerate -m "create new post table"
# # alembic upgrade head dab mn change ka lia hain version update krna ka lia ya command use krty hain
# # # alembic revision --autogenerate -m "create new column column nameg mail in todos_work  table"