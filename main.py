from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db
app = Flask(__name__)
users = web.UserStore()
tasks_list = [0,"Hello","Welcome",1,"2","3"]
@app.route('/')
def index():
    if web.auth.name != "":
        return redirect("/home")
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html", name=web.auth.name,tasks=tasks_list)

@app.route('/tasks')
def tasks():
    return render_template("new.html", name=web.auth.name)

@app.route('/new')
def new():
    return render_template("new.html", name=web.auth.name)

@app.route('/about')
def about():
    return render_template("about.html", name=web.auth.name)
app.run(host='0.0.0.0', port=81,debug=True)