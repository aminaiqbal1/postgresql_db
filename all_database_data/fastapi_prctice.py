# . Create a Simple "Hello World" API
# Task: Create a basic FastAPI app that returns "Hello, World!" when you make a GET request to the root endpoint (/).

from fastapi import FastAPI
app = FastAPI()
@app.get("/hello_world")
async def hello_world():
    return {"message": "Hello World"}
# 2. Create a User Registration Endpoint
# Task: Create an endpoint /register that accepts user registration details (username, email, password) and returns a success message.
# Objective: Learn about request bodies and data validation in FastAPI.
@app.post("/sinup/{username}/{email}/{password}")
async def sinup(username, email, password):
    try:
        return {"username": username,
                "email": email,
                "password": password,
                "message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e),
                "message": "User registration failed"}
@app.post("/register")
async def register(username: str, email: str, password: str):
    try:
        return {"username": username,
                "email": email,
                "password": password,
                "message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}
from pydantic import BaseModel
class Login(BaseModel):
    username : str
    email: str
    password: int
@app.get("/login")
async def login(login_de :Login):
    try:
        return {"details": login_de,
                "massage": "login details sucsefuly submit"}
    except Exception as e:
        return {"error": e,
                "message": "login details failed"}

# 3. Create a User Login Endpoint with Authentication
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Mock user data (for demo purposes)
mock_user_db = {
    "amina": "password123",
    "nabiha": "pass456"
}

# Request body schema
class LoginRequest(BaseModel):
    username: str
    password: str

# Authentication logic as a dependency
def authenticate_user(login: LoginRequest):
    stored_password = mock_user_db.get(login.username)
    if not stored_password or stored_password != login.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return login.username

# Login endpoint
@app.post("/login")
def login(user: str = Depends(authenticate_user)):
    return {"message": f"Welcome, {user}!"}



# 4. Create CRUD Operations for Managing Items
# Task: Create a simple API to manage items (e.g., products, tasks, or notes). Implement the following operations:
# Create a new item.
# Read (get) an item by its ID.
# Update an item by its ID.
# Delete an item by its ID.

# Objective: Learn about CRUD operations, handling query parameters, and path parameters.

# Steps:

# Create a Pydantic model to validate item data (e.g., name, description).

# Create endpoints for each CRUD operation (POST, GET, PUT, DELETE).

# Use an in-memory store (e.g., a list or dictionary) for storing items for now.

# 5. Create a To-Do List API with Status Update
# Task: Create an API that manages a to-do list. Each to-do item should have a title, description, and a completion status (true/false).

# Objective: Learn about request bodies, query parameters, and database-like interactions.

# Steps:

# Create a Todo Pydantic model with fields like title, description, and completed (boolean).

# Create routes for:

# Adding a new to-do.

# Getting a list of all to-dos.

# Updating the completion status of a to-do.

# Deleting a to-do by its ID.

# Use an in-memory data structure (e.g., a list of dictionaries) to store to-dos.

# 6. Create an API that Takes Query Parameters
# Task: Create an endpoint that accepts query parameters and filters a list of items based on them (e.g., search for books by author or genre).

# Objective: Learn about query parameters and filtering data.

# Steps:

# Create a route /books that accepts query parameters like author and genre.

# Use query parameters to filter a list of predefined books.

# Return a filtered list based on the query parameters (e.g., /books?author=J.K.Rowling).

# 7. Use SQLAlchemy with FastAPI (Database Integration)
# Task: Set up a PostgreSQL or SQLite database, and use SQLAlchemy to manage data. Create a CRUD API for managing a resource (e.g., tasks, notes, users).

# Objective: Learn how to interact with a database using SQLAlchemy and FastAPI.

# Steps:

# Install SQLAlchemy and database libraries (e.g., pip install sqlalchemy psycopg2).

# Define a SQLAlchemy model for the resource (e.g., Task).

# Create the database tables using SQLAlchemy and FastAPI.

# Implement CRUD operations (create, read, update, delete) on the database.

# Use SQLAlchemy session for database transactions.

# 8. Create an API with JWT Authentication
# Task: Secure an endpoint using JWT (JSON Web Tokens). Create endpoints for user registration, login, and accessing a protected resource (e.g., /profile).

# Objective: Learn about JWT authentication in FastAPI.

# Steps:

# Implement user registration and login as before.

# Create a function to generate JWT tokens on successful login.

# Protect a /profile route by requiring a valid JWT token.

# Use Depends to verify the JWT token in a custom dependency function.

# 9. Create a File Upload API
# Task: Create an API that allows users to upload files (e.g., images, documents). The API should save the files to disk and return the file URL.

# Objective: Learn how to handle file uploads in FastAPI.

# Steps:

# Use the File and UploadFile classes from FastAPI to handle file uploads.

# Create an endpoint that accepts a file upload (POST /upload).

# Save the uploaded file to a directory on the server.

# Return the URL to access the uploaded file.

# 10. Create Pagination in an API
# Task: Create an API that supports pagination for large datasets (e.g., a list of items, blog posts, etc.).

# Objective: Learn about pagination in FastAPI and managing large datasets.

# Steps:

# Create an endpoint that returns a list of items (e.g., posts).

# Accept query parameters limit and skip for pagination.

# Ensure that the returned data is paginated, meaning it returns only a subset of the data.

# Bonus Tasks:
# Task 1: Build an API that can send email notifications to users when certain actions occur (e.g., after a successful registration or when a new post is published).

# Task 2: Add CORS support to your FastAPI application to allow cross-origin requests from your front-end application.

# Recommended Approach:
# Start Simple: Begin with basic tasks like creating a "Hello World" API and CRUD endpoints.

# Gradually Add Complexity: Once you're comfortable with the basics, add features like authentication, database integration, or JWT authentication.

# Use Documentation: As you encounter challenges, refer to the FastAPI documentation to deepen your understanding.

# Practice and Experiment: The more you practice, the more comfortable you'll get with FastAPI and backend development in general.

# Feel free to reach out if you need help with any specific task!
import uvicorn
if __name__ == "__main__":
    uvicorn.run("fastapi_prctice:app", host="127.0.0.1", port=8000, reload=True)
# python fastapi_prctice.py