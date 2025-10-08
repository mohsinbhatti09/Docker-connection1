from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB using environment variables
mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")
mongo_host = os.getenv("MONGO_HOST", "mongo")

client = MongoClient(f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017/")
db = client["testdb"]
collection = db["items"]

@app.route('/')
def home():
    return "Welcome to Simple CRUD API!"

# Create
@app.route('/create', methods=['POST'])
def create():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Created", "data": data}), 201

# Read
@app.route('/read', methods=['GET'])
def read():
    items = list(collection.find({}, {"_id": 0}))
    return jsonify(items)

# Update
@app.route('/update/<name>', methods=['PUT'])
def update(name):
    new_data = request.json
    collection.update_one({"name": name}, {"$set": new_data})
    return jsonify({"message": "Updated"})

# Delete
@app.route('/delete/<name>', methods=['DELETE'])
def delete(name):
    collection.delete_one({"name": name})
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
