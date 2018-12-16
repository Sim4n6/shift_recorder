from flask import Flask, url_for, redirect, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/login')
def login():
    return render_template("login_form.html")


@app.route('/login_check', methods=['POST', 'GET'])
def login_check():
    if request.method == 'POST':
        app.logger.debug("a request has been made from client to server : asking to POST some data :\n" + "username : ")
        app.logger.debug(request.form["username"] + " - " + request.form["password"] + "button: " + request.form["submit_btn"])
        if request.form["submit_btn"] == "new user":
            return redirect(url_for("create_new_user"))
        else:
            return "ok data to be checked: " + request.form["username"] + " ... " + request.form["password"]
    else:
        print("a requestfor a GET made")
        return "a request has been made from a client to server : asking for something"


@app.route('/create_new_user_check', methods=['GET', 'POST'])
def create_new_user():
    if request.method == 'GET':
        return render_template("new_user_form.html")
    elif request.method  == 'POST':
        return "create new user with data: " + request.form["name"]
    else:
        return "else request method "
