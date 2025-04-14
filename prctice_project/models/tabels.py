from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
# Post Model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    tittle = Column(String, nullable=True)
    name = Column(String, nullable=True)
    # user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    # user = relationship("User", back_populates="posts")