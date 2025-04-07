from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Relationship with Post
class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)  # Primary key for unique identification
    hastag = Column(String, nullable=False)  # Cannot be empty
    content = Column(String, nullable=False)  # Cannot be empty

    # Define relationship with Todo
    todo = relationship("Todo", back_populates="post")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)  # Primary key for unique identification
    name = Column(String, nullable=False)  # Cannot be empty
# Relationship with Todo
class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)  # Primary key for unique identification
    title = Column(String, nullable=False)  # Cannot be empty
    description = Column(String, nullable=True)  # Can be empty
    gmail = Column(String, unique = True)  # Optional Gmail field
    completed = Column(Integer, default=0)  # 0: Not completed, 1: Completed

    # Foreign key for posts table with ondelete
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    post = relationship("Post", back_populates="todo")
    user = relationship("todo", back_populates="post")


 # relationship with post table
    # s ko ab hum alumbic .env file mn base model ko import krynga 
# alembic revision --autogenerate -m "create new post table"
# alembic upgrade head dab mn change ka lia hain version update krna ka lia ya command use krty hain
# # alembic revision --autogenerate -m "create new column column nameg mail in todos_work  table"