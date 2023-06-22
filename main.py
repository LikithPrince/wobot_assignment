from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic
from typing import List
from pydantic import BaseModel
from bson.objectid import ObjectId
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
from functions import *
from config import *


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# HTTP Basic authentication
security = HTTPBasic()


class Todo(BaseModel):
   title       : str
   subject     : str


''' This is the home route that welcomes the user'''
@app.get("/")
def home():
   return {"message": "Welcome to the To-do list API."}


'''Route for user registration. User has to set their username and password for the 1st time,
if the user is already registered, it says username already registered, else user get registered
successfully. The username and password will store in the mongodb.'''
@app.post("/register")
def register(username: str, password: str):
   user = get_user(username)
   if user:
      raise HTTPException(status_code=400, detail="Username already registered")
   auth = wobot_auth_collection.insert_one({"username": username, "password" : password})
   
   return {"message": "User registered successfully"}


# Route for user login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
   user = authenticate_user(form_data.username, form_data.password)
   if not user:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Invalid username or password",
         headers={"WWW-Authenticate": "Bearer"},
      )
   access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token = create_access_token(
      data={"sub": user}, expires_delta=access_token_expires
   )
   return {"access_token": access_token, "token_type": "bearer", "message": "Login successful"}


# # to get all the todo list
@app.get("/todos", response_model=List[Todo])
def get_todos():
   todos = list(collection.find())
   return todos

## to get individual todo with id
@app.get("/todos/{todo_id}")
def get_todo(todo_id: str):
   todo = collection.find_one({"_id": ObjectId(todo_id)})
   if todo:
      todo["_id"] = str(todo["_id"])  # Convert ObjectId back to string
      return todo
   else:
      raise HTTPException(status_code=404, detail="Todo not found.")


# to create new todo
@app.post("/todos")
def create_todo(todo: Todo):
   todo_dict = todo.dict()
   result = collection.insert_one(todo_dict).inserted_id
   return {"message": "Todo created successfully.", "id": str(result)}


# to update todo or add new todo to same id
@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, updated_todo: Todo):
   updated_dict = dict(updated_todo)
   # result = collection.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_dict})    ## to replace
   result = collection.update_one({"_id": ObjectId(todo_id)}, {"$push": {"todos": updated_dict}})   ## to add 
   if result.modified_count == 1:
      return {"message": "Todo updated successfully."}
   else:
      raise HTTPException(status_code=404, detail="Todo not found.")


# to delete todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
   result = collection.delete_one({"_id": ObjectId(todo_id)})
   if result.deleted_count == 1:
      return {"message": "Todo deleted successfully."}
   else:
      raise HTTPException(status_code=404, detail="Todo not found.")



@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
   try:
      payload = jwt.decode(token, key = SECRET_KEY, algorithms = [ALGORITHM])
      username = payload.get("sub")
      if not username:
         raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid authentication token",
               headers={"WWW-Authenticate": "Bearer"},
         )
      user = get_user(username)
      if not user:
         raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid username",
               headers={"WWW-Authenticate": "Bearer"},
         )
      return {"message": "Access granted"}
   except JWTError:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Invalid authentication token",
         headers={"WWW-Authenticate": "Bearer"},
      )
   

