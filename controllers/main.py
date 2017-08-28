from flask import *
from extensions import db

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
	loggedin = False
	albums = ()

	username = ''
	if 'username' in session:
		loggedin = True
		username = session['username']

	cur = db.cursor()
	cur.execute("SELECT username FROM User")
	results = cur.fetchall()

	cur.execute("SELECT * FROM Album WHERE access = 'public'")
	albums = cur.fetchall()

	if loggedin:
		cur.execute("SELECT DISTINCT * FROM (SELECT * FROM Album A WHERE A.access = 'public' UNION SELECT * FROM Album A1 WHERE A1.username = '"+username+"' UNION SELECT * FROM Album A2 WHERE A2.albumid IN (SELECT AA.albumid FROM AlbumAccess AA WHERE AA.username = '"+username+"')) AS temp")
		albums = cur.fetchall()

	options = {
    "usernames": results,
    	"nav_home": True,
    	"albums": albums
    }
	return render_template("index.html", **options)
