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

def getData(dep : str):
	v = (dep,)
	db.execute("SELECT * FROM `EQUIPMENT` WHERE `DEPARTMENT` = (%s)", v)
	data = db.fetchall()
	return render_template("tables.html", data=data, arr=arr, dep=dep)

@app.route("/cardiac")
def cardiac():
	return getData("cardiac")

@app.route("/chathetar")
def chathetar():
	return getData("chathetar")


@app.route("/dental")
def dental():
	return getData("dental")

def get(s : str):
	value = request.form.get(s)
	if value == None:
		value = ""
	return value

@app.route("/addelement", methods=["GET", "POST"])
def addElement():
	if request.method == "GET":
		return render_template("addelmnt.html", loggedin=check_logged_in())
	elif request.method == "POST":
		sql = ("INSERT INTO EQUIPMENT (DEPARTMENT, ID, SERIAL_NUMBER, MANUFACTURER, MODEL,"
			  " INDATE, OPERATION_DATE, SUPPLIER, WARRANTY_PERIOD, PRICE, MAINTAINANCE_COMPANY,"
			  " MAINTAINANCE_CONTRACT_TYPE, START_END_CONTRACT_DATE, RECIPIENT_NAME,"
			  " RECIPIENT_PHONE, MANUFACTURER_COUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,"
			  " %s, %s, %s, %s, %s, %s, %s)")
		val = (get("department"), get("eqName"), get("serialNumber"), get("manufacturer"),
		get("model"), get("inDate"), get("opDate"), get("supplier"), get("period"), get("price"),
		get("company"), get("cType"), get("cDate"), get("rName"), get("rPhone"), get("country"))
		db.execute(sql, val)
		mydb.commit()
		return render_template("addelmnt.html", loggedin=check_logged_in(), message="Equipment Added successfully!")


def report(dep : str, reportType):
	v = (dep, )
	print(reportType)
	db.execute("SELECT * FROM `{}` WHERE `DEPARTMENT` = (%s)".format(reportType), v)
	data = db.fetchall()
	rows = []
	arr = []
	arr2 = []
	ids = []
	lens = []
	i = 0
	while i < len(data):
		temp = []
		temp2 = []
		last = data[i][2]
		arr.append(last)
		arr2.append(data[i][1])
		while i < len(data) and last == data[i][2]:
			temp.append(data[i][3])
			temp2.append(data[i][2] + str(i))
			ids.append(temp2)
			i += 1
		lens.append(len(temp))
		rows.append(temp)
	return render_template("Checkform.html", dep=dep, rows=rows, lens=lens, arr=arr, len=len(rows), arr2=arr2, reportType=reportType, ids=ids)

def maintainanceReport(dep : str, reportType):
	v = (dep, )
	db.execute("SELECT * FROM `{}` WHERE `DEPARTMENT` = (%s)".format(reportType), v)
	data = db.fetchall()
	arr = []
	arr2 = []
	i = 0
	while i < len(data):
		last = data[i][2]
		arr.append(last)
		arr2.append(data[i][1])
		while i < len(data) and last == data[i][2]:
			i += 1
	for i in range(len(arr)):
		sql = ("INSERT INTO MAINTANANCE_REPORTS (DEPARTMENT, EQUIPMENT_SERIAL_NUMBER,"
			   " EQUIPMENT_NAME, DATA) VALUES (%s, %s, %s, %s);")
		val = (dep, arr2[i], arr[i], request.form.get(arr[i]))
		db.execute(sql, val)
		mydb.commit()
	if reportType[0] == 'S':
		return redirect(url_for(dep + 'Sterilization'))
	else:
		return redirect(url_for(dep + 'PPMReports'))

@app.route("/cardiac/ppmreport", methods = ["GET", "POST"])
def cardiacPPMReports():
	if request.method == "GET":
		return report("cardiac", 'PPM_REPORTS')
	elif request.method == "POST":
		return maintainanceReport("cardiac", 'PPM_REPORTS')

@app.route("/chathetar/ppmreport", methods = ["GET", "POST"])
def chathetarPPMReports():
	if request.method == "GET":
		return report("chathetar", 'PPM_REPORTS')
	elif request.method == "POST":
		return maintainanceReport("chathetar", 'PPM_REPORTS')

@app.route("/dental/ppmreport", methods = ["GET", "POST"])
def dentalPPMReports():
	if request.method == "GET":
		return report("dental", 'PPM_REPORTS')
	elif request.method == "POST":
		return maintainanceReport("dental", 'PPM_REPORTS')

@app.route("/cardiac/sterilization", methods = ["GET", "POST"])
def cardiacSterilization():
	if request.method == "GET":
		return report("cardiac", 'STERILIZATION')
	elif request.method == "POST":
		return maintainanceReport("cardiac", 'STERILIZATION')

@app.route("/chathetar/sterilization", methods = ["GET", "POST"])
def chathetarSterilization():
	if request.method == "GET":
		return report("chathetar", 'STERILIZATION')
	elif request.method == "POST":
		return maintainanceReport("chathetar", 'STERILIZATION')

@app.route("/dental/sterilization", methods = ["GET", "POST"])
def dentalSterilization():
	if request.method == "GET":
		return report("dental", 'STERILIZATION')
	elif request.method == "POST":
		return maintainanceReport("dental", 'STERILIZATION')



if __name__ == "__main__":
	app.run(debug = True)
