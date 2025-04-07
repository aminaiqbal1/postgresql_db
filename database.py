
from sqlalchemy import create_engine # for making connection with fastapi
from sqlalchemy.orm import sessionmaker # for creating session

DATABASE_URL = "postgresql://neondb_owner:npg_NhkBxZ6Ob8Fr@ep-floral-sound-a899twvx-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL) # for making connection with fastapi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # hum na us ko engin ka sath baind kr dia yani database ka  sath  for creating session