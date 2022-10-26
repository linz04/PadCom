from flask import Flask,render_template,request
import subprocess,os
from subprocess import PIPE

app = Flask(__name__)


@app.route('/')
def Compiler():
	check=''
	return render_template('home.html', check=check)


@app.route('/submit',methods=['GET','POST'])
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
	return render_template('home.html',code=code, input=inp, output=output, check=check)

def complier_output(code,inp,chk):
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