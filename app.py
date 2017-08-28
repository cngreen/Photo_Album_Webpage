from flask import Flask, render_template
import extensions
import controllers
import config

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

### TODO ###
secret_prefix = '/xjicc5ld/p3'


## Replace controllers below
app.register_blueprint(controllers.album, url_prefix=secret_prefix)
app.register_blueprint(controllers.albums, url_prefix=secret_prefix)
app.register_blueprint(controllers.pic, url_prefix=secret_prefix)
app.register_blueprint(controllers.main, url_prefix=secret_prefix)
app.register_blueprint(controllers.user, url_prefix=secret_prefix)
app.register_blueprint(controllers.login, url_prefix=secret_prefix)

app.register_blueprint(controllers.user_api, url_prefix=secret_prefix)
app.register_blueprint(controllers.login_api, url_prefix=secret_prefix)
app.register_blueprint(controllers.album_api, url_prefix=secret_prefix)
app.register_blueprint(controllers.pic_api, url_prefix=secret_prefix)

app.secret_key = '\xe59\xee\x93`\xd8\xfa\xe8\x00\x9f\xc7\x8d|\xec\xe3U\xad\xab\x88#\xe7\xa6\xda\xf9'

###########################

# Register the controllers
#app.register_blueprint(controllers.album)
#app.register_blueprint(controllers.albums)
#app.register_blueprint(controllers.pic)
#app.register_blueprint(controllers.main)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html'), 404

@app.errorhandler(403)
def forbidden(e):
	return render_template('forbidden.html'), 403

def get_fullname(user):
    cur = extensions.db.cursor()
    cur.execute("SELECT firstname, lastname FROM User WHERE username='"+user+"'")
    result = cur.fetchone()
    return result['firstname'] + " " + result['lastname']

app.jinja_env.globals.update(get_fullname=get_fullname)
# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
