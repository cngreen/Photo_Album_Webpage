from flask import *
from extensions import *
import re

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/user/edit')
def user_edit_route():
	if 'username' not in session:
	    return redirect(url_for('login.login_route'))	
        return render_template("user_edit.html") 

@user.route('/user')	
def user_route():
	if 'username' in session:
		return redirect(url_for('user.user_edit_route'))
	return render_template("user.html")
