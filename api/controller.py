from config import *
from flask import render_template, request, redirect, url_for, session, abort, flash
from flask_login import login_required
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import subprocess,os
from markupsafe import Markup
from subprocess import PIPE
import db
import uuid


@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('fullname', None)
	return redirect(url_for('login'))

@app.route("/api/login", methods = ["GET", "POST"])
def login_handler():
	if request.method == 'POST':
		mysql = db.connect()
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user where email = %s', (email, ))
		rv = cursor.fetchone()
		if(rv is not None):
			if bcrypt.check_password_hash(rv['password'], password):
				session['loggedin'] = True
				session['id'] = rv['id']
				session['fullname'] = rv['fullname']
				session['lecturer'] = rv['isLecturer']
				msg = 'Logged in successfully !'
				flash(msg)
				cursor.close()
				mysql.close()
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong username or password!")
				cursor.close()
				mysql.close()
				return redirect(url_for('login'))
		else:
			flash("Wrong username or password!")
			cursor.close()
			mysql.close()
			return redirect(url_for('login'))

@app.route("/api/register", methods = ["GET", "POST"])
def register_handler():
	if request.method == 'POST':
		mysql = db.connect()
		fullname = request.form['name']
		email = request.form['email']
		password = request.form['password']
		confirm = request.form['con-password']
		if password != confirm:
			flash("Password is not same")
			return redirect(url_for('register'))
		password = bcrypt.generate_password_hash(password).decode('utf-8')
		cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
			flash(msg)
			return redirect(url_for('register'))
		else:
			cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, 0)', (email, password, fullname, ))
			mysql.commit()
			msg = 'You have successfully registered !'
			flash(msg)
			cursor.close()
			mysql.close()
		return redirect(url_for('register'))

@app.route('/api/submit',methods=['GET','POST'])
def submit():
	if request.method == 'POST':

		code = request.form['code']
		inp = request.form['input']
		chk = request.form.get('check')

		if  not chk == '1':
			inp = ""
			check = ''
		else:
			check = 'checked'	

		output=complier_output(code,inp,chk)
	return render_template('code.html',code=code, input=inp, output=output, check=check)

@app.route("/api/notes", methods=["GET", "POST"])
def notes_handler():
	if request.method == "POST":
		mysql = db.connect()
		uid = uuid.uuid4().hex
		title = request.form["title"]
		notes = request.form['notes']
		out = Markup(notes)
		print("Notes: ", out, flush=True)
		cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO notes VALUES (NULL, %s, %s, %s, 0)', (session['id'], password, fullname, ))
		return render_template("note.html", output=out, notes=notes, title=title)

@app.route("/note")
def note_gen():
	uid = uuid.uuid4().hex
	return redirect(url_for('note_view', uuid=uid))

@app.route("/note/<uuid>", methods=["POST", "GET"])
def note_view(uuid):
	if request.method == "POST":
		mysql = db.connect()
		title = request.form["title"]
		notes = request.form['notes']
		user_id = f"[{int(session['id'])}]"
		out = Markup(notes)
		print("Notes: ", out, flush=True)
		cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO notes VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, content = %s', (uuid, user_id, title, notes, title, notes, ))
		mysql.commit()
		cursor.close()
		mysql.close()
		return render_template("note.html", output=out, notes=notes, title=title)
	else:
		return render_template("note.html")


def complier_output(code,inp,chk):
	print("user_id: ", session['id'], flush=True)
	if not os.path.exists('code/Try.c'):
		os.open('code/Try.c', os.O_CREAT)	
	fd = os.open("code/Try.c", os.O_WRONLY)
	os.truncate(fd,0)
	fileadd=str.encode(code)
	os.write(fd,fileadd)
	os.close(fd) 
	s = subprocess.run(['gcc','-o','code/new','code/Try.c'], stderr=PIPE,)
	check = s.returncode
	if check == 0:
		if chk == '1':
			r = subprocess.run(["./code/new"], input=inp.encode(), stdout=PIPE)
		else:
			r = subprocess.run(["./code/new"], stdout=PIPE)
		return r.stdout.decode("utf-8")
	else:
		return s.stderr.decode("utf-8")


if __name__=='__main__':
	app.run(debug=True)