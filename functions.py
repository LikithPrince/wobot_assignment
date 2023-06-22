from config import *
from datetime import datetime, timedelta
from jose import jwt


# Secret key for JWT
SECRET_KEY = "likith"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

''' This function takes username as string and search for username in the database[MongoDB], 
if username present in the database it will return username, else None '''
def get_user(username: str):
   userName = wobot_auth_collection.find_one({"username" : username})
   if userName:
      if userName['username'] == username:
         return userName['username']
   return None

# Function to authenticate user
''' This function takes username and password in string format as input parameters
and 1st find the username in the database, if not found, it return false.
if it found, then it search for password, if password found, it will match with the
password entered by user, if both are matching, it return username, else return false'''
def authenticate_user(username: str, password: str):
   user = get_user(username)
   if not user:
      return False
   passWord = wobot_auth_collection.find_one({"password" : password})
   if passWord['password'] != password:
      return False
   return user


# Function to create access token
'''This function takes username in dictionary and expire time for the token
and encode to the form of json web token and return that token'''
def create_access_token(data: dict, expires_delta: timedelta):
   to_encode = data.copy()
   expire = datetime.utcnow() + expires_delta
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt