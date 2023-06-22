from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://likithprince:<pw>@cluster0.mjxrwzx.mongodb.net/")

db = client["todo_app"]

collection = db["todos"]

wobot_auth_collection = db['wobot_auth']