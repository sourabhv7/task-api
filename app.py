from flask import Flask, request, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

uri = "mongodb://localhost:27017/task-api"

app = Flask(__name__)
app.secret_key = 'my-secret-key'
app.config["MONGO_URI"] = uri

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route("/register",methods = ['POST','GET'])
def register():
    email = request.args.get('email')
    password = request.args.get('password')
    print(email)
    print(password)
    if mongo.db.users.find_one({'email': email}):
        return {'error':'User already exist'}
    
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    entry = {
        'email':email,
        'password': hashed
    }
    mongo.db.users.insert_one(entry)
    return {'status':'Registartion Success'}

@app.route("/login",methods = ['POST','GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    if not mongo.db.users.find_one({'email':email}):
        return {'error':'User not found.'}

    user_data = mongo.db.users.find_one({'email':email})
    old_password = user_data['password']
    if bcrypt.check_password_hash(old_password, password):
        session['user'] = email
        return {'status':'You are logged-in.'}
    return {'error':'Password mismatched.'}

app.run()