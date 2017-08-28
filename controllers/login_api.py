from flask import *
from extensions import *

login_api = Blueprint('login_api', __name__, template_folder='templates')

@login_api.route('/api/v1/login', methods = ['POST'])
def login_api_route():
    errormsg = []
    data = request.get_json()
    if data == None:
        return (jsonify(errors=[{'message':"You did not provide the necessary fields"}]), 422)
    if 'username' not in data or 'password' not in data:
        errormsg.append("You did not provide the necessary fields")
        tojson = []
        for msg in errormsg:
            tojson.append({'message': msg})
        return (jsonify(errors=tojson), 422)

    username = data['username']
    password = data['password']

    if 'username' == "":
        errormsg.append("Username may not be left blank")
    if 'password' == "":
        errormsg.append("Password may not be left blank")

    if len(errormsg) != 0:
        tojson = []
        for msg in errormsg:
            tojson.append({'message': msg})
        return (jsonify(errors=tojson), 422)

    else:
        cur = db.cursor()
        cur.execute("SELECT * FROM User WHERE username='"+username+"'")
        user = cur.fetchone()
        if user == None:
            errormsg.append("Username does not exist")
            tojson = []
            for msg in errormsg:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 404)

        elif check_password(password, user['password']):
            session['username'] = user['username']
            return jsonify(username=username)

        else:
            errormsg.append("Password is incorrect for the specified username")
            tojson = []
            for msg in errormsg:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 422)

@login_api.route('/api/v1/logout', methods = ['POST'])
def logout_api_route():
    if 'username' not in session:
        tojson = []
        tojson.append({'message': 'You do not have the necessary credentials for the resource'})
        return (jsonify(errors=tojson), 401)
    session.clear()
    return (jsonify(), 204)
