import os
import hashlib
from flask import *
from extensions import *

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_type(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

album = Blueprint('album', __name__, template_folder='templates')

def get_pics(albumid):
	# error checking
	contain = db.cursor()
	contain.execute("SELECT Contain.picid, Contain.sequencenum, Contain.caption, Photo.format, Photo.date FROM Contain, Photo WHERE Contain.albumid = '"+albumid+"' AND Contain.picid = Photo.picid ORDER BY Contain.sequencenum")
	pics = contain.fetchall()
	contain.execute("SELECT title FROM Album WHERE albumid = '"+albumid+"'")
	albumname = contain.fetchall()
	return pics, albumname

def get_users(albumid):
	contain = db.cursor()
	contain.execute("SELECT username FROM AlbumAccess WHERE albumid = '"+albumid+"'")
	users = contain.fetchall()
	return users

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
        albumid = None
        if 'username' not in session:
            return redirect(url_for('login.login_route'))
        if 'albumid' in request.form:
                albumid = request.form['albumid']
        if 'albumid' in request.args:
                albumid = request.args['albumid']
        if albumid == None:
            abort(404)
        dbcur = db.cursor()
        dbcur.execute("SELECT * FROM Album WHERE albumid = '"+albumid+"'")
        if dbcur.rowcount == 0:
            abort(404)
        resultz = dbcur.fetchall()
        if resultz[0]['username'] != session['username']:
            abort(403)

	if request.method == 'POST':
		if ('access' in request.form):
			albumid = request.form.get('albumid')
			update = db.cursor()
			update.execute("UPDATE Album SET access = '"+request.form.get('access')+"' WHERE Album.albumid = '"+albumid+"'")
			update.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE Album.albumid = '"+albumid+"'")

			if (request.form.get('access') == 'public'):
				update.execute("DELETE FROM AlbumAccess WHERE AlbumAccess.albumid = '"+albumid+"'")

			return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
		if 'op' not in request.form:
			return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
		if request.form.get('op') == 'add':
			if 'file' not in request.files:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			if 'albumid' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))

			albumid = request.form.get('albumid')
			file = request.files['file']
			if file.filename == '':
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			if file and allowed_type(file.filename):
				filename = file.filename
				extension = filename[-3:]
				filename = filename.replace(' ', '')[:-4].upper()
				m = hashlib.md5(str(request.form.get('albumid') + filename))
				filename = m.hexdigest()
				uploadfilename = filename + '.' + extension
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploadfilename))
				insert = db.cursor()
				insert.execute("INSERT INTO Photo (picid, format) VALUES ('"+filename+"', '"+extension+"')")
				insert.execute("SELECT sequencenum FROM Contain ORDER BY sequencenum DESC LIMIT 1")
				result = insert.fetchone()['sequencenum']
				sequencenum = str(int(result) + 1)
				insert.execute("INSERT INTO Contain (sequencenum, albumid, caption, picid) VALUES ('"+sequencenum+"', '"+request.form.get('albumid')+"', '', '"+filename+"')")
				insert.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE Album.albumid = '"+albumid+"'")

		if request.form.get('op') == 'delete':
			if 'picid' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			if 'albumid' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			picid = request.form.get('picid')
			albumid = request.form.get('albumid')
			quer = db.cursor()
			quer.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE Album.albumid = '"+albumid+"'")
			quer.execute("SELECT Photo.format FROM Photo WHERE picid='"+picid+"'")
			the_photo = quer.fetchone()
			delete_photo(picid, the_photo['format'])

		if request.form.get('op') == 'grant':
			if 'albumid' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			if 'username' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			username = request.form.get('username')
			albumid = request.form.get('albumid')
			quer = db.cursor()

			if (username == ''):
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			quer.execute("SELECT * FROM User WHERE username = '"+username+"'")
			if (quer.rowcount == 0):
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			quer.execute("SELECT * FROM AlbumAccess WHERE username = '"+username+"' AND albumid = '"+albumid+"'")
			if 	(quer.rowcount > 0):
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			quer.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE Album.albumid = '"+albumid+"'")
			quer.execute("INSERT INTO AlbumAccess (albumid, username) VALUES ('"+albumid+"', '"+username+"')")

		if request.form.get('op') == 'revoke':
			if 'albumid' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			if 'username' not in request.form:
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			username = request.form.get('username')
			albumid = request.form.get('albumid')
			quer = db.cursor()
			quer.execute("SELECT * FROM AlbumAccess WHERE username = '"+username+"' AND albumid = '"+albumid+"'")
			if 	(quer.rowcount == 0):
				return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
			quer.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE Album.albumid = '"+albumid+"'")
			quer.execute("DELETE FROM AlbumAccess WHERE username='"+username+"' AND albumid = '"+albumid+"'")

		return redirect(url_for('album.album_edit_route', albumid=request.form.get('albumid')))
	# TODO: allow photos to be deleted / added
	if albumid == None:
		if 'albumid' not in request.args:
			abort(404)
		albumid = request.args.get('albumid')
	pics, albumname = get_pics(albumid)
	users = get_users(albumid)
	private = False
	quer = db.cursor()
	quer.execute("SELECT access FROM Album WHERE albumid = '"+albumid+"'")
	if quer.fetchone()['access'] == 'private':
		private = True

	options = {
		"edit": True,
		"pics": pics,
		"albumname": albumname,
		"albumid": albumid,
		"users": users,
		"private": private
	}
	return render_template("album_edit.html", **options)

@album.route('/album')
def album_route():
	return render_template("album.html")
