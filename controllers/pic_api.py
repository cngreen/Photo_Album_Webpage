from flask import *
from extensions import *

pic_api = Blueprint('pic_api', __name__, template_folder='templates')

def get_previous(picid):
    contain = db.cursor()
    count = contain.execute("SELECT Photo.picid, Photo.format,Contain.albumid, Contain.sequencenum FROM Contain, Photo WHERE Contain.albumid IN (SELECT albumid FROM Contain WHERE picid = '"+picid+"') AND Photo.picid = Contain.picid AND Contain.sequencenum < (SELECT sequencenum FROM Contain WHERE picid = '"+picid+"') ORDER BY Contain.sequencenum DESC LIMIT 1")
    if count > 0: 
        previous = contain.fetchone()
        previd = previous['picid']
        hasprevious = True
    else:
        previous = ()
        hasprevious = False
        previd = ''
    return previous, hasprevious, previd

def get_next(picid):
    contain = db.cursor()
    count = contain.execute("SELECT Photo.picid, Photo.format,Contain.albumid, Contain.sequencenum FROM Contain, Photo WHERE Contain.albumid IN (SELECT albumid FROM Contain WHERE picid = '"+picid+"') AND Photo.picid = Contain.picid AND Contain.sequencenum > (SELECT sequencenum FROM Contain WHERE picid = '"+picid+"') ORDER BY Contain.sequencenum LIMIT 1")
    if count > 0:
        next = contain.fetchone()
        hasnext = True
        nextid = next['picid']
    else:
        next = ()
        hasnext = False
        nextid = ''
    return next, hasnext, nextid

@pic_api.route('/api/v1/pic/<picid>', methods=['GET', 'PUT'])
def pic_api_route(picid):
    query = db.cursor()
    query.execute("SELECT * FROM Photo WHERE picid = '"+str(picid)+"'")
    if query.rowcount == 0: #album doesn't exist
    	tojson = []
        tojson.append({'message': 'The requested resource could not be found'})
        return (jsonify(errors=tojson), 404)
    if request.method == 'GET':
        previous, hasprevious, previd = get_previous(picid)
        next, hasnext, nextid = get_next(picid)
        ismypic = False

        quer = db.cursor()
        quer.execute("SELECT Contain.albumid FROM Contain WHERE Contain.picid = '"+str(picid)+"'")              
        albumid = quer.fetchone()['albumid']

        isPrivate = False
        quer.execute("SELECT access FROM Album WHERE albumid = '"+str(albumid)+"'")
        privacy = quer.fetchone()['access']
        if (privacy == 'private'):
            isPrivate = True

        if 'username' not in session:
            ismypic = False
            if isPrivate:
                tojson = []
                tojson.append({'message': 'You do not have the necessary credentials for the resource'})
                return (jsonify(errors=tojson), 401)
        else:
            username = session['username']
            quer.execute("SELECT username FROM Album WHERE albumid = '"+str(albumid)+"'")
            
            if(quer.fetchone()['username'] == username):
                ismypic = True

            else:
                if isPrivate:
                    result = quer.execute("SELECT * FROM AlbumAccess WHERE albumid = '"+str(albumid)+"' AND username = '"+username+"'")
                    if (result == 0):
                        tojson = []
                        tojson.append({'message': 'You do not have the necessary permissions for the resource'})
                        return (jsonify(errors=tojson), 403)
        cur = db.cursor()
        cur.execute("SELECT Photo.picid, Photo.format, Contain.sequencenum, Contain.albumid, Contain.caption FROM Contain, Photo WHERE Contain.picid = '"+picid+"' AND Photo.picid = Contain.picid")
        my_pics = cur.fetchall()
        for pic in my_pics:
            albumid = pic['albumid']
            caption = pic['caption']
            format = pic['format']
            picid = pic['picid']
        return jsonify(albumid=albumid, caption=caption, format=format, next=nextid, picid=picid, prev=previd)
    if request.method == 'PUT':
    	data = request.get_json()
        previous, hasprevious, previd = get_previous(picid)
        next, hasnext, nextid = get_next(picid) 
        ismypic = False

        quer = db.cursor()
        quer.execute("SELECT Contain.albumid FROM Contain WHERE Contain.picid = '"+str(picid)+"'")              
        albumid = quer.fetchone()['albumid']

        isPrivate = False
        quer.execute("SELECT access FROM Album WHERE albumid = '"+str(albumid)+"'")
        privacy = quer.fetchone()['access']
        if (privacy == 'private'):
            isPrivate = True

        if 'username' not in session:
            ismypic = False
            if isPrivate:
                tojson = []
                tojson.append({'message': 'You do not have the necessary credentials for the resource'})
                return (jsonify(errors=tojson), 401)

        else:
            username = session['username']
            quer.execute("SELECT username FROM Album WHERE albumid = '"+str(albumid)+"'")
            
            if(quer.fetchone()['username'] == username):
                ismypic = True

            else:
                if isPrivate:
                    result = quer.execute("SELECT * FROM AlbumAccess WHERE albumid = '"+str(albumid)+"' AND username = '"+username+"'")
                    if (result == 0):
                        tojson = []
                        tojson.append({'message': 'You do not have the necessary permissions for the resource'})
                        return (jsonify(errors=tojson), 403)
        newcaption = ""
        if 'caption' in data:
            newcaption = data['caption']
        quer.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE Album.albumid = '"+str(albumid)+"'")
        quer.execute("UPDATE Contain SET caption = '"+newcaption+"' WHERE Contain.picid = '"+str(picid)+"'")
        cur = db.cursor()
        cur.execute("SELECT Photo.picid, Photo.format, Contain.sequencenum, Contain.albumid, Contain.caption FROM Contain, Photo WHERE Contain.picid = '"+picid+"' AND Photo.picid = Contain.picid")
        my_pics = cur.fetchall()
        for pic in my_pics:
            albumid = pic['albumid']
            caption = pic['caption']
            format = pic['format']
            picid = pic['picid']    
        return (jsonify(albumid=albumid, caption=caption, format=format, next=nextid, picid=picid, prev=previd), 200)
