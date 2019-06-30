import os
from app import app
from flask import render_template, request, redirect
from models import formopener
import datetime

from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'database' 

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:nhDqzQgoXgsSLi3D@cluster0-izzqz.mongodb.net/database?retryWrites=true&w=majority' 

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index', methods = ["GET", "POST"])
# This is where you create an account
def index():
    socialnetwork = mongo.db.socialnetwork
    # users = socialnetwork.find()
    if request.method == "GET": 
        return render_template("index.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        print(username + password)
        # socialnetwork = mongo.db.socialnetwork
        socialnetwork.insert({"username" : username, "password" : password, "posts" : []})
        return render_template('login.html')
    # connect to the database

# CONNECT TO DB, ADD DATA

# This is where you login
@app.route('/login', methods = ["GET", "POST"])
def check_login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        socialnetwork = mongo.db.socialnetwork
        username = request.form["username"]
        password = request.form["password"]
        user = socialnetwork.find({"username" : username})
        print(user)
        for person in user: 
            print(person["username"] + person["password"])
            if password == person["password"]:
                return render_template('/homepage.html', username = username)
            else:
                return "Your password is wrong"
        return "Your username is incorrect"

#this is where you add a post   
@app.route('/homepage', methods = ["GET", "POST"])
def post(username):
    if request.method == "GET":
        return render_template("homepage.html")
    else:
        mypost = request.form["mypost"]
        # username = request.form["username"]
        time = datetime.datetime.now()
        print(mypost)
        # print(username)
        posts = mongo.db.posts
        posts.insert({"username" : username, "post" : mypost, "time" : time})
        #go to database
        allposts = mongo.db.posts
        #make a collection of posts
        posts = allposts.find({})
        #display
        return render_template("allposts.html", posts = posts)
        
        # socialnetwork = mongo.db.socialnetwork
        # person = socialnetwork.find({"username": username})
        # mongo.db.socialnetwork.find_one_and_update({"username" : username}, {"$post" : "test"})
        # print(person["post"])
        # person["posts"].append(mypost)
        # return("done")
@app.route('/allposts')
def allposts():
    #go to database
    allposts = mongo.db.posts
    #make a collection of posts
    posts = allposts.find({})
    #display
    return render_template("allposts.html", posts = posts)

@app.route('/name/<name>')

def name(name):
    #go to database
    allposts = mongo.db.posts
    #make a collection of posts
    posts = allposts.find({"username": name})
    #display
    return render_template("singleuserposts.html", posts = posts, name = name)