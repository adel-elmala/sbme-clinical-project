import os
from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
# import mysql.connector, json, json2table, json2html
import mysql.connector
from mysql.connector import errorcode

arr = ['Name', 'Depatment', 'Manufactrer', 'Model', 'Serial Number', 'Manufacturer Country',
 'In Date', 'Operation Date', 'Warranty Period', 'Supplier', 'Price', 'Maintainance Company',
  'Mainyainance Contract Type', 'Start/End Date of Contract', 'Recipient Name', 'Recipient Phone']

app = Flask(__name__)
 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
 
#set db as global variable
db = ""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="mydata"
)
db = mydb.cursor()

def check_logged_in():
	session.get('username')
	v = (session.get("username"), session.get("password"))
	db.execute("SELECT * FROM USERS WHERE USERNAME = (%s) AND PASSWORD = (%s) LIMIT 1", v)
	data = db.fetchone()
	if data is not None:
		return True
	return False

@app.route("/")
def home():
	return render_template("home.html", loggedin=check_logged_in())

@app.route("/signin", methods = ["GET", "POST"])
def signin():
	#check_logged_in()
	if request.method == "GET":
		return render_template("signin.html", message = "")
	elif request.method == "POST":	
		username = request.form.get("username")
		password = request.form.get("password")
		v = (username, password)
		db.execute("SELECT * FROM `USERS` WHERE `USERNAME` = (%s) AND `PASSWORD` = (%s)", v)
		data = db.fetchone()
		session['username'] = username
		session['password'] = password
		if data is not None:
			return redirect(url_for('home'))
		return render_template("signin.html", message = "wrong username or password")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template("signup.html")
	elif request.method == "POST":
		Fname = request.form.get("firstname")
		Lname = request.form.get("lastname")
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		phone = request.form.get("phone")
		sql = "INSERT INTO USERS (FIRSTNAME,LASTNAME, USERNAME, EMAIL, PASSWORD, PHONE) VALUES (%s, %s, %s, %s, %s, %s)"
		val = (Fname, Lname, username, email, password, phone)
		db.execute(sql, val)
		mydb.commit()  
		return redirect(url_for('signin'))

@app.route("/contact_form", methods = ["GET", "POST"])
def contact_form():
	if request.method == "GET":
		return render_template("contact_form.html", loggedin=check_logged_in())

@app.route("/signout")
def signout():
	session['username'] = None
	session['password'] = None
	return redirect(url_for('home'))

def getData(dep : str):
	v = (dep,)
	db.execute("SELECT * FROM `EQUIPMENT` WHERE `DEPARTMENT` = (%s)", v)
	data = db.fetchall()
	return render_template("tables.html", data=data, loggedin=check_logged_in(), arr=arr)

@app.route("/cardiac")
def cardiac():
	return getData("Cardiac")

@app.route("/chatheter")
def chatheter():
	return getData("Chatheter")


@app.route("/dental")
def dental():
	return getData("Dental")

if __name__ == "__main__":
	app.run(debug = True)