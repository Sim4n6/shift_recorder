from flask import Flask, url_for, redirect, request, render_template, flash, session
import xlsxwriter as xwr
import sqlite3 as lite
from hashlib import sha1


def encrypt_password(password):
    return sha1(password.encode('UTF-8')).hexdigest()


def initialize_db(db_name):
    try:
        conn0 = lite.connect(db_name)
        c0 = conn0.cursor()
        c0.execute('''CREATE TABLE IF NOT EXISTS user(employee_id INTEGER PRIMARY KEY, username TEXT NOT NULL, 
                    name TEXT NOT NULL, password TEXT NOT NULL );''')
        conn0.commit()
    except lite.Error as e:
        conn0.rollback()
        app.logger.error("An error occurred : " + e.args[0])
    finally:
        conn0.close()


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zZERUNdnJE'


@app.route('/')
@app.route('/index')
def index():
    initialize_db("shifts.db")
    if 'username' in session:
        return redirect(url_for("shift_add"))
    return redirect(url_for("login_check"))


@app.route('/login', methods=['POST', 'GET'])
def login_check():
    if request.method == 'POST':
        if request.form["submit_btn"] == "new user":
            return redirect(url_for("create_new_user"))
        else:
            try:
                # Establish Connection
                conn3 = lite.connect('shifts.db')
                c3 = conn3.cursor()
                # Find user If there is any take proper action
                find_user = '''SELECT * FROM user WHERE username = ? and password = ?'''
                c3.execute(find_user, [request.form["username"], encrypt_password(request.form["password"])])
                result = c3.fetchall()

                if result:
                    session['username'] = request.form['username']
                    return redirect(url_for("shift_add"), request.form["username"])
                else:
                    flash('could not connect !')
            except lite.Error as e:
                conn3.rollback()
                app.logger.error("An error occurred : ", e.args[0])
            finally:
                conn3.close()
            return redirect(url_for("login_check"))
    elif request.method == 'GET':
        return render_template("login_form.html")
    else:
        return "a request has been made from a client to server : asking for something"


@app.route('/create_new_user', methods=['GET', 'POST'])
def create_new_user():
    if request.method == 'GET':
        return render_template("new_user_form.html")
    elif request.method == 'POST':
        try:
            conn4 = lite.connect("shifts.db")
            c4 = conn4.cursor()
            # Find Existing username if any take proper action
            find_user = '''SELECT DISTINCT username, name FROM user WHERE username = ? and name = ? '''
            c4.execute(find_user, [request.form["username"], request.form["name"]])
            if c4.fetchall():
                flash('Username taken try a different one, please.')
            else:
                # defined a function for encrypting password
                conn4.create_function('encrypt', 1, encrypt_password)
                # Create New Account
                insert = '''INSERT INTO user (username, name, password) VALUES(?, ?, encrypt(?))'''
                c4.execute(insert, [request.form["username"], request.form["name"], request.form["password"]])
                conn4.commit()
        except lite.Error as e:
            conn4.rollback()
            app.logger.error("An error occurred : " + e.args[0])
        finally:
            conn4.close()
        return redirect(url_for("login_check"))
    else:
        return "else request method "


@app.route("/shift_add")
def shift_add():
    if 'username' in session:
        return render_template("shift_add.html")
    return redirect(url_for("logout"))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
