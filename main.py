from better_profanity import profanity
import re
from flask import Flask, render_template, redirect, request, current_app, request
from replit import web, db
app = Flask(__name__)
users = web.UserStore()
@app.route('/')
def index():
    if web.auth.name != "":
        return redirect("/home")
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/home',methods=["POST", "GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def home():
    if request.method == "POST":
        url = request.form["url"]
        users.current["url"] = url
    if web.auth.name not in db["names"]:
        users.current["tasks"] = []
        users.current["id"] = 0
        users.current["url"] = request.headers["X-Replit-User-Profile-Image"]
        db["names"].append(web.auth.name)
    return render_template("home.html", name=web.auth.name,tasks=users.current["tasks"][0:],url=users.current["url"])

@app.route('/tasks')
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def tasks():
    return redirect("/new")

@app.route('/new' , methods=["POST", "GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def new():
    if request.method == "POST":
        if len(users.current["tasks"])%3 > 20:
            return "You have reached your max amount of task remove some so you can make more"
        users.current["id"]=users.current["id"]+1
        new_tasks = users.current["tasks"]
        title = profanity.censor(request.form["title"],censor_char="🤬")
        desc = profanity.censor(request.form["desc"],censor_char="🤬")
        if len(title) > 75 or len(desc) > 500 or len(title) == 0 or len(desc) == 0:
            return "You Title or Description is to long or short"
        new_tasks.append(users.current["id"])
        new_tasks.append(re.sub("<.*?>","",title))
        new_tasks.append(re.sub("<.*?>","",desc))
        if len(new_tasks)%3 == 0:
            users.current["tasks"] = new_tasks
            return redirect("/home")
        else:
            return "something went wrong"
        print(users.current["tasks"])
    return render_template("new.html", name=web.auth.name,url=users.current["url"])

@app.route('/about')
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def about():
    return render_template("about.html", name=web.auth.name,url=users.current["url"])

@app.route("/search", methods=["POST", "GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def search():
    what_search = request.args.get("search").lower()
    if what_search == "home":
        return redirect("/home")
    elif "make" in what_search or "new" in what_search:
        return redirect("/new")
    elif "about" in what_search:
        return redirect("/about")
    elif "replit" in what_search:
        return redirect("https://replit.com/")
    elif "like" in what_search:
        return redirect("/__repl")
    elif "follow" in what_search:
        return redirect("https://replit.com/@GoodVessel92551")
    elif what_search == "remove all tasks":
        users.current["tasks"] = []
        return redirect("/home")
    elif what_search == "reset profile image":
        users.current["url"] = request.headers["X-Replit-User-Profile-Image"]
        return redirect("/home")
    return redirect("/home")

@app.route('/edit' , methods=["POST", "GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def edit():
    if request.method == "POST":
        id = request.args.get("id")
        print(id)
        new_tasks = users.current["tasks"]
        title = profanity.censor(request.form["title"],censor_char="🤬")
        desc = profanity.censor(request.form["desc"],censor_char="🤬")
        if len(title) > 75 or len(desc) > 500 or len(title) == 0 or len(desc) == 0:
            return "You Title or Description is to long or short"
        for i in range(len(new_tasks)):
            if int(id) == new_tasks[i]:
                new_tasks[i+1] = re.sub("<.*?>","",title)
                new_tasks[i+2] = re.sub("<.*?>","",desc)
                break
        if len(new_tasks)%3 == 0:
            users.current["tasks"] = new_tasks
            return redirect("/home")
        else:
            return "something went wrong"
    else:
        current_tasks = users.current["tasks"]
        id = request.args.get("id")
        print(id)
        for i in range(len(current_tasks)):
            if current_tasks[i] == int(id):
                title2 = current_tasks[i+1]
                desc2 = current_tasks[i+2]
                return render_template("edit.html", name=web.auth.name, title=title2, desc=desc2,url=users.current["url"])
        return redirect("/home")

@app.route('/remove')
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def remove():
    id = request.args.get("id")
    current_tasks = users.current["tasks"]
    for i in range(len(current_tasks)):
        if current_tasks[i] == int(id):
            current_tasks.pop(i)
            current_tasks.pop(i)
            current_tasks.pop(i)
            break
    if len(current_tasks)%3 == 0:
        users.current["tasks"] = current_tasks
        return redirect("/home")
    else:
        return "something went wrong"

@app.route("/admin")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def admin():
    if web.auth.name != "GoodVessel92551":
        return redirect("/home")
    else:
        return render_template("admin.html",names=db["names"][0:])
    
app.run(host='0.0.0.0', port=81,debug=False)