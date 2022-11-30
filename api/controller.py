from config import *
from flask import render_template, request, redirect, url_for, session, abort, flash, send_file
from flask_login import login_required
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import subprocess,os
from markupsafe import Markup
from subprocess import PIPE
import db
import uuid
import pdfkit
import pwd


def notes_checker(user_id, uid):
	mysql = db.connect()
	cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM notes where JSON_CONTAINS(user_id, \"{user_id}\") AND notes_id = \"{uid}\"")
	rv = cursor.fetchone()
	if (rv is not None):
		return True
	else:
		return False

def codes_checker(user_id, uid):
	mysql = db.connect()
	cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM codes where JSON_CONTAINS(user_id, \"{user_id}\") AND codes_id = \"{uid}\"")
	rv = cursor.fetchone()
	if (rv is not None):
		return True
	else:
		return False

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))

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


@app.route("/note")
def note_gen():
	uid = uuid.uuid4().hex
	return redirect(url_for('notes_handler', uuid=uid))

@app.route("/code")
def code_gen():
	uid = uuid.uuid4().hex
	return redirect(url_for('codes_handler', uuid=uid))

@app.route('/code/<uuid>',methods=['GET','POST'])
def codes_handler(uuid):
	try:
		if request.method == 'POST':
			mysql = db.connect()
			code = request.form['code']
			try:
				inp = request.form['input']
				title = request.form['title']
			except:
				title = ""
			action = request.form['action']
			user_id = f"[{int(session['id'])}]"
			if(action == "Run"):
				chk = request.form.get('check')

				if  not chk == '1':
					inp = ""
					check = ''
				else:
					check = 'checked'	

				output=complier_output(code,inp,chk,uuid)
				return render_template('code.html',code=code, input=inp, output=output, check=check, title=title, uid=uuid)
			else:
				cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO codes VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, content = %s', (uuid, user_id, title, code, title, code, ))
				mysql.commit()
				cursor.close()
				mysql.close()
			return render_template("code.html", code=code, title=title, uid=uuid)
		else:
			if(session['loggedin'] == None):
				return redirect(url_for('home'))
			#check if codes have owner or not
			mysql = db.connect()
			cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT codes_id, title, content from codes where codes_id = %s', (uuid, ))
			rv = cursor.fetchone()
			print(rv, flush=True)
			if(rv != None and codes_checker(session['id'], uuid) == True):
				cursor.close()
				mysql.close()
				return render_template("code.html", code=rv['content'], title=rv['title'], uid=rv['codes_id'])
			elif(rv == None):
				#if no owner add owner
				user_id = f"[{int(session['id'])}]"
				cursor.execute('INSERT INTO codes VALUES (%s, %s, NULL, NULL)', (uuid, user_id, ))
				mysql.commit()
				cursor.close()
				mysql.close()
				return render_template("code.html", uid=uuid)
			else:
				return redirect(url_for('dashboard'))
	except:
		return redirect(url_for('home'))


@app.route("/share-code/<uuid>", methods=["POST", "GET"])
def code_share(uuid):
	if request.method == "POST":
		email = request.form['email']
		mysql = db.connect()
		cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT id FROM user WHERE email=%s", (email,))
		if cursor.rowcount == 1:
			#check user already in code or not
			rv = cursor.fetchone()
			cursor.execute(f"SELECT * FROM codes where user_id LIKE \"%{rv['id']}%\" and codes_id = \"{uuid}\"")
			if cursor.rowcount == 0:
				cursor.execute("UPDATE codes SET user_id = JSON_ARRAY_INSERT(user_id, '$[0]', %s) where codes_id = %s", (rv['id'], uuid))
				mysql.commit()
				cursor.close()
				mysql.close()
				msg = f"Success invite user {email}"
				flash(msg)
				return redirect(url_for('codes_handler', uuid=uuid))
			else:
				flash("User already Invited!")
				return redirect(url_for('codes_handler', uuid=uuid))
		else:
			cursor.close()
			mysql.close()
			flash("User Not Found!")
			return redirect(url_for('codes_handler', uuid=uuid))

@app.route("/share-note/<uuid>", methods=["POST", "GET"])
def note_share(uuid):
	if request.method == "POST":
		email = request.form['email']
		mysql = db.connect()
		cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT id FROM user WHERE email=%s", (email,))
		if cursor.rowcount == 1:
			#check user already in notes or not
			rv = cursor.fetchone()
			cursor.execute(f"SELECT * FROM notes where user_id LIKE \"%{rv['id']}%\" and notes_id = \"{uuid}\"")
			if cursor.rowcount == 0:
				cursor.execute("UPDATE notes SET user_id = JSON_ARRAY_INSERT(user_id, '$[0]', %s) where notes_id = %s", (rv['id'], uuid))
				mysql.commit()
				cursor.close()
				mysql.close()
				msg = f"Success invite user {email}"
				flash(msg)
				return redirect(url_for('notes_handler', uuid=uuid))
			else:
				flash("User already Invited!")
				return redirect(url_for('notes_handler', uuid=uuid))
		else:
			cursor.close()
			mysql.close()
			flash("User Not Found!")
			return redirect(url_for('notes_handler', uuid=uuid))

@app.route("/note/<uuid>", methods=["POST", "GET"])
def notes_handler(uuid):
	try:
		if request.method == "POST":
			mysql = db.connect()
			title = request.form["title"]
			notes = request.form['notes']
			action = request.form['action']
			user_id = f"[{int(session['id'])}]"
			out = Markup(notes)
			print("Action: ", action, flush=True)
			if(action == "Save"):
				cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO notes VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, content = %s', (uuid, user_id, title, notes, title, notes, ))
				mysql.commit()
				cursor.close()
				mysql.close()
			elif(action == "View"):
				print("Masuk")
				return redirect(url_for('notes_view', uuid=uuid))
			elif(action == "Download"):
				return redirect(url_for('notes_download', uuid=uuid))
			return render_template("note.html", output=out, notes=notes, title=title, uid=uuid)
		else:
			#check if notes have owner or not
			mysql = db.connect()
			cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT notes_id, title, content from notes where notes_id = %s', (uuid, ))
			rv = cursor.fetchone()
			if(rv != None and notes_checker(session['id'], uuid) == True):
				out = Markup(rv['content'])
				cursor.close()
				mysql.close()
				return render_template("note.html", output=out, notes=rv['content'], title=rv['title'], uid=rv['notes_id'])
			elif(rv == None):
				#if no owner add owner
				user_id = f"[{int(session['id'])}]"
				cursor.execute('INSERT INTO notes VALUES (%s, %s, NULL, NULL)', (uuid, user_id, ))
				mysql.commit()
				cursor.close()
				mysql.close()
				return render_template("note.html", uid=uuid)
			else:
				return redirect(url_for('dashboard'))
	except:
		return redirect(url_for('home'))

@app.route("/view/<uuid>")
def notes_view(uuid):
	mysql = db.connect()
	cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT title, content from notes where notes_id = %s', (uuid, ))
	rv = cursor.fetchone()
	out = Markup(rv['content'])
	print(rv, flush=True)
	return out

@app.route("/download/<uuid>")
def notes_download(uuid):
	config = pdfkit.configuration(wkhtmltopdf = "/usr/bin/wkhtmltopdf")
	url = request.url.replace("download", "view")
	print(url)
	path = "notes/"+uuid+".pdf"
	print(path)
	pdfkit.from_url(url, path, verbose=True, configuration = config)
	print("="*50)
	return send_file(path, as_attachment=True)
	#return "test"




def complier_output(code,inp,chk,name):
	username = "nobody"
	pwent = pwd.getpwnam(username)
	uid = pwent.pw_uid
	gid = pwent.pw_gid
	folder = f"code/{name}"
	path = folder+"/Try.c"
	elf = folder+"/new"
	if not os.path.exists(path):
		os.makedirs(folder, mode=0o777)
		os.open(path, os.O_CREAT)	
	fd = os.open(path, os.O_WRONLY)
	os.truncate(fd,0)
	fileadd=str.encode(code)
	os.write(fd,fileadd)
	os.close(fd) 
	os.chown(path, uid, gid)
	s = subprocess.run(['gcc','-o',elf,path], stderr=PIPE,)
	check = s.returncode
	os.setgid(gid)
	os.setuid(uid)
	os.system('id')
	if check == 0:
		if chk == '1':
			r = subprocess.run([elf], input=inp.encode(), stdout=PIPE)
		else:
			r = subprocess.run([elf], stdout=PIPE)
		return r.stdout.decode("utf-8")
	else:
		return s.stderr.decode("utf-8")


if __name__=='__main__':
	app.run(debug=True)