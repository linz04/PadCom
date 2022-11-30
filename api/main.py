from config import *
from db import *
from controller import *
from routes import *
# from hr import *
from flask_cors import CORS
import os
import pwd

CORS(app)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    username = "nobody"
    pwent = pwd.getpwnam(username)
    uid = pwent.pw_uid
    gid = pwent.pw_gid
    os.setgid(gid)
    os.setuid(uid)
    os.system('id')
    app.run(debug=True,host="0.0.0.0",threaded=True)