#********************************************************************************
#--------------------------------------------------------------------------------
#
#	Significance Labs
#	Brooklyn, NYC
#
# 	Author: Alexandra Berke (aberke)
# 	Written: June 2014
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************




from flask import Flask, send_file, redirect
from flask.ext.compress import Compress

from cleaner import auth



# Configuration ----------------------------------------------

app = Flask('app')
app.config.from_object('config')
Compress(app)

from cleaner import cleaner as cleaner_blueprint
app.register_blueprint(cleaner_blueprint, url_prefix='/cleaner')


#---------------------------------------------- Configuration #

@app.route('/style-guide')
def style_guide():
	return send_file('static/html/style-guide.html')


@app.route('/')
@app.route('/new')
@app.route('/sign-in')
@app.route('/reset-password')
def no_user_views():
	"""
	Redirect to '/dashboard' if user is signed in 
	"""
	if auth.get_user():
		return redirect('/dashboard')
	return base()


@app.route('/dashboard')
@app.route('/list/<id>')
def user_views(id=None):
	""" 
	Redirect to '/' if no user signed in
	"""
	if not auth.get_user():
		return redirect('/')
	return base()



@app.route('/test')
def base():
	return send_file('static/html/base.html')














