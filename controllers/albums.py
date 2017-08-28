from flask import *
from extensions import *

albums = Blueprint('albums', __name__, template_folder='templates')

def get_albums(username, myAlbum):
	# error checking
	test_username = db.cursor()
	test_username.execute("SELECT * FROM User WHERE username = '"+username+"'")
	if(test_username.rowcount == 0):
		abort(404)
	# query for the albums
	cur = db.cursor()
	if (myAlbum):
		cur.execute("SELECT * FROM Album WHERE username = '"+username+"'")
	else:
		cur.execute("SELECT * FROM Album WHERE username = '"+username+"' AND access = 'public'")
	albums = cur.fetchall()
	return albums

@albums.route('/albums/edit', methods=['GET', 'POST'])
def albums_edit_route():
	if 'username' not in session:
		return redirect(url_for('login.login_route'))
	username = session['username']
	if 'username' in request.args:
			if (request.args.get('username') != username):
				abort(403)
	albums= get_albums(username, True)
	if 'op' in request.form:
		if request.form.get('op') == "add":
			# Add a new album
			if 'title' not in request.form:
				return redirect(request.url)
			if len(request.form.get('title')) > 50:
				return redirect(request.url)
			insr = db.cursor()
			insr.execute("INSERT INTO Album (title, username, access) VALUES ('"+request.form.get('title')+"', '"+username+"', 'private')")
			return redirect(request.url)
		if request.form.get('op') == "delete":
			# Delete an existing album
			if 'albumid' not in request.form:
				return redirect(request.url)
			# Find all existing photos in the album
			finder = db.cursor()
			finder.execute("SELECT Photo.picid, Photo.format FROM Contain, Photo WHERE Contain.albumid='"+request.form.get('albumid')+"' AND Contain.picid=Photo.picid")
			to_delete = finder.fetchall()
			for dphoto in to_delete:
				delete_photo(dphoto['picid'], dphoto['format'])
			deleter = db.cursor()
			deleter.execute("DELETE FROM Album WHERE albumid="+request.form.get('albumid'))
			return redirect(request.url)
	options = {
		"edit": True,
		"albums": albums,
		"username": username
	}
	return render_template("albums.html", **options)


@albums.route('/albums')
def albums_route():
	username = ''
	myAlbum = False
	morealbums = False
	extra = ()

	if 'username' not in session:
		if 'username' not in request.args:
			return redirect(url_for('login.login_route'))
		username = request.args.get('username')
		myAlbum = False

	else:
		username = session['username']
		myAlbum = True
		if 'username' in request.args:
			myAlbum = False
			if (request.args.get('username') != username):
				userNav = request.args.get('username')
				morestuff = db.cursor()
				morestuff.execute("SELECT * FROM Album A WHERE A.username = '"+userNav+"' AND A.albumid IN (SELECT C.albumid FROM AlbumAccess C WHERE C.username = '"+username+"')")
				if (morestuff.rowcount != 0):
					extra = morestuff.fetchall()
					morealbums = True


	if 'username' in request.args:
		username = request.args.get('username')
	
	albums = get_albums(username, myAlbum)

	options = {
		"edit": False,
		"albums": albums,
		"morealbums": morealbums,
		"extra": extra,
		"username": username,
		"ismyalbum": myAlbum
	}
	return render_template("albums.html", **options)
