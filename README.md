# postgresql_db

🔹 What i am  Learn:


Setting up a FastAPI project with AI components

Configuring and connecting to a PostgreSQL database

Implementing CRUD (Create, Read, Update, Delete) operations

Managing database migrations for seamless schema evolution

# NOW START FULL MTHODE OF POSTGRESSQL

sub say phaly hum na 2 ya 3 laibrari install krni hain pip install sqlalchemy alembic psycopg2

install first step


3 alembic init alembic # init ka agy project ka name dalna hai hum na project ka name bhi alembic rakha hai 


2 pip install psycopg2

1 pip install alembic


2 step ab hum ak command use krynga alembic init alembic s say ak folder bana ga of ak alumbic.init name ki file banagi 


3 step 


ab hum alembic init name wali file mn sqlchemy url ka agy apni database ka url paste krynga mn neon tech name ki database ko use kr rhi hon 

4 

us ka baad ak folder banynga models name ka us ka under jis name ka tables banana hain us name ki file banyn ga us ka baad hum us ka alumbic  ka folder ka under .env ka under 


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
