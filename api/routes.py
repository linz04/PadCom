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

@app.route("/home")
def home():
	return render_template("home.html")