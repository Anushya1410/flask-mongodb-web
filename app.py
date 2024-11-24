from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv  


load_dotenv()

app = Flask(__name__)


app.secret_key = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['testdb']
collection = db['users']

@app.route('/')
def index():
    users = list(collection.find())
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    if name and email:
        collection.insert_one({'name': name, 'email': email})
        flash("User added successfully!", "success")
    else:
        flash("Please fill out all fields.", "danger")
    return redirect('/')

@app.route('/delete/<user_id>')
def delete_user(user_id):
    try:
        collection.delete_one({'_id': ObjectId(user_id)})
        flash("User deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting user: {e}", "danger")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
