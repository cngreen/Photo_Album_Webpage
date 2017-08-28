from flask import *
from extensions import *
import re

user_api = Blueprint('user_api', __name__, template_folder='templates')

def check_valid_password(password1, password2, errorMessage):
    error = False
    errormsg = ""
    numbers = sum(c.isdigit() for c in password1)
    alpha   = sum(c.isalpha() for c in password1)
    scores  = sum(c == "_"    for c in password1)
    others  = len(password1) - numbers - alpha - scores
    if len(password1) < 8:
        errorMessage.append("Passwords must be at least 8 characters long")
    if numbers == 0 or alpha == 0:
        errorMessage.append("Passwords must contain at least one letter and one number")
    if others > 0:
        errorMessage.append("Passwords may only contain letters, digits, and underscores")
    if password1 != password2:
        errorMessage.append("Passwords do not match")

def check_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def check_valid_username(username, errorMessage):
    numbers = sum(c.isdigit() for c in username)
    alpha   = sum(c.isalpha() for c in username)
    scores  = sum(c == "_"    for c in username)
    others  = len(username) - numbers - alpha - scores
    if others > 0:
        errorMessage.append("Usernames may only contain letters, digits, and underscores")

@user_api.route('/api/v1/user', methods=['GET', 'POST', 'PUT'])
def user_api_route():
    if request.method == 'GET':
        if 'username' not in session:
            tojson = []
            tojson.append({'message': 'You do not have the necessary credentials for the resource'})
            return (jsonify(errors=tojson), 401)

        username = session['username']
        cur = db.cursor()
        cur.execute("SELECT firstname, lastname, email FROM User WHERE username = '"+username+"'")
        my_users = cur.fetchall()
        for user in my_users:
            firstname = user['firstname']
            lastname = user['lastname']
            email = user['email']
        return jsonify(username=username, firstname=firstname, lastname=lastname, email=email)

#****PUT****
    elif request.method == 'PUT':
        data = request.get_json()

        if 'username' not in session:
            tojson = []
            tojson.append({'message': 'You do not have the necessary credentials for the resource'})
            return (jsonify(errors=tojson), 401)

        if data == None:
            return (jsonify(errors=[{'message':"You did not provide the necessary fields"}]), 422)
        if ('firstname' not in data) or ('lastname' not in data) or ('password1' not in data) or ('password2' not in data) or ('email' not in data):
            return (jsonify(errors=[{'message':"You did not provide the necessary fields"}]), 422)

        firstname = ""
        lastname = ""
        password1 = ""
        password2 = ""
        email = ""

        username = session['username']
        if 'firstname' in data:
            firstname = data['firstname']
        if 'lastname' in data:
            lastname = data['lastname']
        if 'password1' in data:
            password1 = data['password1']
        if 'password2' in data:
            password2 = data['password2']
        if 'email' in data:
            email = data['email']

        errormsg = []
        error = False

        cur = db.cursor()
        if firstname != "":
            if len(firstname) > 20:
                errormsg.append("Firstname must be no longer than 20 characters")
            else:
                cur.execute("UPDATE User SET firstname = '"+firstname+"' WHERE username = '"+username+"'")
        if lastname != "":
            if len(lastname) > 20:
                errormsg.append("Lastname must be no longer than 20 characters")
            else:
                cur.execute("UPDATE User SET lastname = '"+lastname+"' WHERE username = '"+username+"'")
        if email != "":
            if len(email) > 40:
                errormsg.append("Email must be no longer than 40 characters")
            elif not check_valid_email(email):
                errormsg.append("Email address must be valid")
            else:
                cur.execute("UPDATE User SET email = '"+email+"' WHERE username = '"+username+"'")
        if (password1 != '') and (password2 != ''):
            check_valid_password(password1, password2, errormsg)
            if len(errormsg) == 0:
                cur.execute("UPDATE User SET password = '"+hash_password(password1)+"' WHERE username = '"+username+"'")

        if len(errormsg) != 0:
            tojson = []
            for msg in errormsg:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 422)
        else:
            cur.execute("SELECT * FROM User WHERE username = '"+username+"'")
            result = cur.fetchone()
            return (jsonify(username=username, firstname=result['firstname'], lastname=result['lastname'], email=result['email']), 200)

#****POST****
    elif request.method == 'POST':
        data = request.get_json()
        if data == None:
            return (jsonify(errors=[{'message':"You did not provide the necessary fields"}]), 422)
        if ('username' not in data) or ('firstname' not in data) or ('lastname' not in data) or ('password1' not in data) or ('password2' not in data) or ('email' not in data):
            return (jsonify(errors=[{'message':"You did not provide the necessary fields"}]), 422)

        username = data['username']
        firstname = data['firstname']
        lastname = data['lastname']
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']

        errorMessage = []

        if len(username) > 20:
            errorMessage.append("Username must be no longer than 20 characters")
        if len(username) < 3:
            errorMessage.append("Usernames must be at least 3 characters long")
        if len(firstname) > 20:
            errorMessage.append("Firstname must be no longer than 20 characters")
        if len(lastname) > 20:
            errorMessage.append("Lastname must be no longer than 20 characters")
        if len(email) > 40:
            errorMessage.append("Email must be no longer than 40 characters")
        if not check_valid_email(email):
            errorMessage.append("Email address must be valid")
        check_valid_username(username, errorMessage)
        check_valid_password(password1,password2,errorMessage)
        cur = db.cursor()
        count = cur.execute("SELECT * FROM User WHERE username = '"+username+"'")
        if count > 0:
            error = True
            errorMessage.append("This username is taken")

        if len(errorMessage) != 0:
            tojson = []
            for msg in errorMessage:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 422)

        else:
            password = hash_password(password1)
            cur.execute("INSERT INTO User (username, firstname, lastname, email, password) VALUES ('"+username+"', '"+firstname+"', '"+lastname+"', '"+email+"', '"+password+"')")
            return (jsonify(username=username, firstname=firstname, lastname=lastname, email=email), 201)
