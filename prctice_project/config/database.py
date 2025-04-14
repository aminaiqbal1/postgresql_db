from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# for making connection with fastapi # for creating session
def get_db():# To get a database connection when needed in FastAPI.Used in FastAPI routes to safely connect to database and auto-close after done.
#  یہ فنکشن ڈیٹا بیس سے محفوظ طریقے سے کنکشن حاصل کرتا ہے اور بعد میں بند کر دیتا

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
DATABASE_URL = "postgresql://neondb_owner:npg_NhkBxZ6Ob8Fr@ep-floral-sound-a899twvx-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL) # for making connection with fastapi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # hum na us ko engin ka sath baind kr dia yani database ka  sath  for creating session
