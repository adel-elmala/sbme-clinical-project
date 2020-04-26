import os
from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
import mysql.connector, json,json2table,json2html
from mysql.connector import errorcode



app = Flask(__name__)
 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
 
#set db as global variable
db = ""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="NEONATAL"
)
db = mydb.cursor()

def check_logged_in():
    db.execute("SELECT * FROM users WHERE username = :username AND password = :password LIMIT 1",
               username = session.get("username"),password = session.get("password"))
    data = db.fetchone()
    if data is not None:
        return render_template("home.html")
    return True

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/signin", methods = ["GET", "POST"])
def signin():
	#check_logged_in()
	if request.method == "GET":
		return render_template("signin.html", message = "")
	elif request.method == "POST":	
		name = request.form.get("ussname")
		password = request.form.get("psswd")
		v = (name,)
		db.execute("SELECT * FROM `docusers` WHERE `username` = (%s)", v)
		data = db.fetchone()
		if data is not None:
			if data[5] == password:
				return render_template("doctors.html")
		db.execute("SELECT * FROM `nurusers` WHERE `username` = (%s)", v)
		data = db.fetchone()
		if data is not None:
			if data[5] == password:
				return render_template("nurses.html")
		db.execute("SELECT * FROM `parusers` WHERE `username` = (%s)", v)
		data = db.fetchone()
		if data is not None:
			if data[5] == password:
				return render_template("parents.html")
		return render_template("signin.html", message = "wrong username or password")


@app.route("/signupdoc", methods = ["GET", "POST"])
def signupdoc():
	if request.method == "GET":
		return render_template("signupdoc.html")
	elif request.method == "POST":
		Fname = request.form.get("fname")
		Lname = request.form.get("lname")
		username = request.form.get("ussname")
		email = request.form.get("mail")
		password = request.form.get("psswd")
		phone = request.form.get("phne")
		identity = request.form.get("ssn")
		major = request.form.get("mjr")
		degree = request.form.get("dgre")
		sql = "INSERT INTO docusers (ID, firstname,lastname, username, email, password, phone, degree, major) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (identity, Fname, Lname, username, email, password, phone, degree, major)
		db.execute(sql, val)
		mydb.commit()  
		return render_template("thanks.html")


@app.route("/signupnur", methods = ["GET", "POST"])
def signupnur():
	if request.method == "GET":
		return render_template("signupnur.html")
	elif request.method == "POST":
		Fname = request.form.get("fname")
		Lname = request.form.get("lname")
		username = request.form.get("ussname")
		email = request.form.get("mail")
		password = request.form.get("psswd")
		phone = request.form.get("phne")
		identity = request.form.get("ssn")
		work_hr = request.form.get("wrk_hr")
		sql = "INSERT INTO nurusers (ID, firstname, lastname, username, email, password, phone, work_hr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		val = (identity, Fname, Lname, username, email, password, phone, work_hr)
		db.execute(sql, val)
		mydb.commit()  
		return render_template("thanks.html")


@app.route("/signuppar", methods = ["GET", "POST"])
def signuppar():
	if request.method == "GET":
		return render_template("signuppar.html")
	elif request.method == "POST":
		Fname = request.form.get("fname")
		Lname = request.form.get("lname")
		username = request.form.get("ussname")
		email = request.form.get("mail")
		password = request.form.get("psswd")
		phone = request.form.get("phne")
		identity = request.form.get("ssn")
		address = request.form.get("adrs")
		sql = "INSERT INTO parusers (ID, firstname,lastname, username, email, password, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		val = (identity, Fname, Lname, username, email, password, phone, address)
		db.execute(sql, val)
		mydb.commit()  
		return render_template("thanks.html")

@app.route("/contact_form", methods = ["GET", "POST"])
def contact_form():
	if request.method == "GET":
		return render_template("contact_form.html")
	msg = request.form.get("message")
	return render_template("thanks.html", "contacting us!")


# my part
@app.route("/doctors", methods = ["GET", "POST"])
def doctors():
	if request.method == "GET":
		db.execute("SELECT * FROM doctor")
		row_headers=[x[0] for x in db.description]
		myresult = db.fetchall()
		json_data=[]
		for result in myresult:
			json_data.append(dict(zip(row_headers,result)))
		jsonfile = json.dumps(json_data)
		return (jsonfile)
		
		# return render_template("doctors.html")

	# return render_template("thankyou.html", "contacting us!")
@app.route("/infants", methods = ["GET", "POST"])
def infants():
	if request.method == "GET":
		db.execute("SELECT * FROM infant")
		row_headers=[x[0] for x in db.description]
		myresult = db.fetchall()
		json_data=[]
		for result in myresult:
			json_data.append(dict(zip(row_headers,result)))
		jsonfile = json.dumps(json_data)
		return (jsonfile)
@app.route("/parents", methods = ["GET", "POST"])
def parents():
	if request.method == "GET":
		db.execute("SELECT * FROM parent")
		row_headers=[x[0] for x in db.description]
		myresult = db.fetchall()
		json_data=[]
		for result in myresult:
			json_data.append(dict(zip(row_headers,result)))
		jsonfile = json.dumps(json_data)
		return (jsonfile)

@app.route("/nurses", methods = ["GET", "POST"])
def nurses():
	if request.method == "GET":
		db.execute("SELECT * FROM nurse")
		row_headers=[x[0] for x in db.description]
		myresult = db.fetchall()
		json_data=[]
		for result in myresult:
			json_data.append(dict(zip(row_headers,result)))
		jsonfile = json.dumps(json_data)
		return (jsonfile)






@app.route("/Equipment", methods = ["GET", "POST"])
def Equipment():
	if request.method == "GET":
		db.execute("SELECT * FROM Equipment")
		row_headers=[x[0] for x in db.description]
		myresult = db.fetchall()
		json_data=[]
		for result in myresult:
			json_data.append(dict(zip(row_headers,result)))
		jsonfile = json.dumps(json_data)
		return (jsonfile)





# end




if __name__ == "__main__":
	app.run(debug = True)