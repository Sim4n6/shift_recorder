from flask import Flask, url_for, redirect, request, render_template, flash, session
import xlsxwriter as xwr
import sqlite3 as lite
from hashlib import sha1


def encrypt_password(password):
	return sha1(password.encode('UTF-8')).hexdigest()


def initialize_db(db_name_arg):
	try:
		conn0 = lite.connect(db_name_arg)
		c0 = conn0.cursor()
		c0.execute('''CREATE TABLE IF NOT EXISTS users(employee_id INTEGER PRIMARY KEY, username TEXT NOT NULL, 
						name TEXT NOT NULL, password TEXT NOT NULL );''')
		conn0.commit()
	except lite.Error as e:
		conn0.rollback()
		app.logger.error("An error occurred : " + e.args[0])
	finally:
		conn0.close()


db_name = "shifts.db"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zZERUNdnJE'
app.config['ENV'] = "developement"


@app.route('/')
@app.route('/index')
def index():
	initialize_db(db_name)
	if 'username' in session:
		return render_template("shift_add.html", user_logged=session["username"])
	return redirect(url_for("login_check"))


@app.route('/login', methods=['POST', 'GET'])
def login_check():
	if request.method == 'POST':
		if request.form["submit_btn"] == "new user":
			return redirect(url_for("register"))
		else:
			try:
				# Establish Connection
				conn3 = lite.connect(db_name)
				c3 = conn3.cursor()
				# Find user If there is any take proper action
				find_user = '''SELECT * FROM user WHERE username = ? and password = ?'''
				c3.execute(find_user, [request.form["username"], encrypt_password(request.form["password"])])
				result = c3.fetchall()

				if result:
					session['username'] = request.form['username']
					return render_template("shift_add.html", user_logged=request.form["username"])
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


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template("register_form.html")
	elif request.method == 'POST':
		try:
			conn4 = lite.connect(db_name)
			c4 = conn4.cursor()
			# Find Existing username if any take proper action
			find_user = '''SELECT DISTINCT username, name FROM user WHERE username = ? and name = ? '''
			c4.execute(find_user, [request.form["username"], request.form["name"]])
			if c4.fetchall():
				flash('Username taken try a different one, please.')
				is_stay = True
			else:
				# defined a function for encrypting password
				conn4.create_function('encrypt', 1, encrypt_password)
				# Create New Account
				insert = '''INSERT INTO user (username, name, password) VALUES(?, ?, encrypt(?))'''
				c4.execute(insert, [request.form["username"], request.form["name"], request.form["password"]])
				conn4.commit()
				flash('new account created successfully ')
				is_stay = False
		except lite.Error as e:
			conn4.rollback()
			app.logger.error("An error occurred : " + e.args[0])
			flash('an error occurred')
		finally:
			conn4.close()
			if is_stay:
				return redirect(url_for("register"))
			else:
				return redirect(url_for("login_check"))

	else:
		return "else request method "


@app.route("/shift_add", methods=['GET', 'POST'])
def shift_add():
	if 'username' in session:
		if request.method == "GET":
			return render_template("shift_add.html", user_logged=session["username"])
		else:
			if request.form["yes_no_btn"] == "yes":
				flash("yes clicked")
			elif request.form["yes_no_btn"] == "no" :
				flash("no clicked")
			return render_template("shift_add.html", user_logged=session["username"])
	else:
		return redirect(url_for("logout"))


@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))


app.run("127.0.0.1", "5000", debug=True)
