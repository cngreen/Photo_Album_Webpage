from flask import *
from extensions import *
import os
import hashlib

album_api = Blueprint('album_api', __name__, template_folder='templates')

def get_pics(albumid):
	contain = db.cursor()
	contain.execute("SELECT Contain.picid, Contain.sequencenum, Contain.caption, Photo.format, Photo.date FROM Contain, Photo WHERE Contain.albumid = '"+albumid+"' AND Contain.picid = Photo.picid ORDER BY Contain.sequencenum")
	pics = contain.fetchall()
	contain.execute("SELECT title FROM Album WHERE albumid = '"+albumid+"'")
	albumname = contain.fetchone()['title']
	return pics, albumname

@album_api.route('/api/v1/album/<albumid>', methods = ['GET'])
def album_api_route(albumid):
    username = ''
    errormsg = []
    quer = db.cursor()
    quer.execute("SELECT access FROM Album WHERE albumid = '"+str(albumid)+"'")
    if quer.rowcount == 0: #album doesn't exist
        errormsg.append("The requested resource could not be found")
        tojson = []
        for msg in errormsg:
            tojson.append({'message': msg})
        return (jsonify(errors=tojson), 404)
    privacy = quer.fetchone()['access']
    if (privacy == 'public'):
        quer.execute("SELECT * FROM Album WHERE albumid = '"+str(albumid)+"'")
        result = quer.fetchone()
        pics, albumname = get_pics(albumid)
        tojson = []
        for pic in pics:
            tojson.append({'albumid': int(albumid), 'caption': pic['caption'], 'date': pic['date'], 'format': pic['format'], 'picid': pic['picid'], 'sequencenum': pic['sequencenum']})
        return(jsonify(access=privacy, albumid=int(albumid), created=result['created'], lastupdated=result['lastupdated'], pics=tojson, title=albumname, username=result['username']))
    else: #is private
        if 'username' not in session:
            errormsg.append("You do not have the necessary credentials for the resource")
            tojson = []
            for msg in errormsg:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 401)
        else:
            checkUser = db.cursor()
            checkUser.execute("SELECT username FROM Album WHERE albumid = '"+str(albumid)+"'")
            if session['username'] == checkUser.fetchone()['username']: #is mine
                quer.execute("SELECT * FROM Album WHERE albumid = '"+str(albumid)+"'")
                result = quer.fetchone()
                pics, albumname = get_pics(albumid)
                tojson = []
                for pic in pics:
		            tojson.append({'albumid': int(albumid), 'caption': pic['caption'], 'date': pic['date'], 'format': pic['format'], 'picid': pic['picid'], 'sequencenum': pic['sequencenum']})
                return(jsonify(access=privacy, albumid=int(albumid), created=result['created'], lastupdated=result['lastupdated'], pics=tojson, title=albumname, username=result['username']))
            else:
                checkUser.execute("SELECT * FROM AlbumAccess WHERE albumid = '"+str(albumid)+"' AND username = '"+session['username']+"'")
                if checkUser.rowcount == 0: #no permission
                    errormsg.append("You do not have the necessary permissions for the resource")
                    tojson = []
                    for msg in errormsg:
                        tojson.append({'message': msg})
                    return (jsonify(errors=tojson), 403)
                else: #have permissions
                    quer.execute("SELECT * FROM Album WHERE albumid = '"+str(albumid)+"'")
                    result = quer.fetchone()
                    pics, albumname = get_pics(albumid)
                    tojson = []
                    for pic in pics:
			            tojson.append({'albumid': int(albumid), 'caption': pic['caption'], 'date': pic['date'], 'format': pic['format'], 'picid': pic['picid'], 'sequencenum': pic['sequencenum']})
                    return(jsonify(access=privacy, albumid=int(albumid), created=result['created'], lastupdated=result['lastupdated'], pics=tojson, title=albumname, username=result['username']))
