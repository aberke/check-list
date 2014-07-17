#********************************************************************************
#--------------------------------------------------------------------------------
#
#	Significance Labs
#	Brooklyn, NYC
#
# 	Author: Alexandra Berke (aberke)
# 	Written: Summer 2014
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from flask import Flask, send_file, redirect
from flask.ext.compress import Compress

import auth



# Configuration ----------------------------------------------

app = Flask('app')
app.config.from_object('config')
Compress(app)

from api import bp as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

from auth import bp as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from backstage import bp as backstage_blueprint
app.register_blueprint(backstage_blueprint, url_prefix='/backstage')

#---------------------------------------------- Configuration #


@app.route('/list/<id>/client')
def client_views(id=None):
	return base()


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


@app.route('/style-guide')
def style_guide():
	return send_file('static/html/style-guide.html')


@app.route('/test')
def base():
	return send_file('static/html/base.html')














