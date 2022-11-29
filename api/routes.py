from config import *
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import login_required
import db

@app.route('/login')
def login():
	return render_template('login.html')

@app.route("/register")
def register():
	return render_template('sign-up.html')

@app.route("/dashboard")
def dashboard():
	return render_template("homelogin.html")

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/code")
def code():
	return render_template("code.html")
