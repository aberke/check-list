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

from help import bp as help_blueprint
app.register_blueprint(help_blueprint, url_prefix='/help')

from info import bp as info_blueprint
app.register_blueprint(info_blueprint, url_prefix='/info')

from language import bp as language_blueprint
app.register_blueprint(language_blueprint, url_prefix='/language')

from backstage import bp as backstage_blueprint
app.register_blueprint(backstage_blueprint, url_prefix='/backstage')

#---------------------------------------------- Configuration #


@app.route('/receipt/<id>')
@app.route('/list/<id>/agreement')
def client_views(id):
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
@app.route('/list/<id>/clean')
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


def base():
	return send_file('static/html/base.html')














