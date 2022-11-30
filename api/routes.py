from config import *
from flask import render_template, request, redirect, url_for, session, abort, jsonify
from flask_login import login_required
import db
import MySQLdb.cursors
import json

@app.route('/login')
def login():
	return render_template('login.html')

@app.route("/register")
def register():
	return render_template('sign-up.html')

@app.route("/dashboard")
def dashboard():
	try:
		if(session['loggedin'] != None):
			mysql = db.connect()
			cursor = mysql.cursor()
			cursor.execute(f"SELECT notes_id, title FROM notes where JSON_CONTAINS(user_id, \"{session['id']}\")")
			row_headers=[x[0] for x in cursor.description] #this will extract row headers
			rv = cursor.fetchall()
			json_data = []
			for result in rv:
				json_data.append(dict(zip(row_headers,result)))
			res = json.dumps(json_data)
			loaded_r = json.loads(res)
			print(loaded_r)
			return render_template("homelogin.html", res=loaded_r)
		else:
			return redirect(url_for('home'))
	except Exception as e:
		print(e)
		return redirect(url_for('home'))

@app.route("/")
def home():
	try:
		if(session['loggedin'] != None):
			return redirect(url_for('dashboard'))
		else:
			return render_template("home.html")
	except:
		return render_template("home.html")


@app.route("/code2")
def code2():
	return render_template("compiler.html")
