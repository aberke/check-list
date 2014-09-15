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
#	Base file of help module
# 	/help/__init__.py
#
# 	The help pages static files were authored by intern Marc Andre using tool:
# 		http://neat-streak.helpdocsonline.com/
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, send_file



bp = Blueprint('help', __name__, static_folder='static')


@bp.route('/')
def index():
	return send_file('help/static/index.html')

@bp.route('/create-an-account/')
def create_an_account():
	return send_file('help/static/create-an-account.html')

@bp.route('/use-menu/')
def menu():
	return send_file('help/static/use-menu.html')

@bp.route('/create-a-new-list/')
def create_a_new_list():
	return send_file('help/static/create-a-new-list.html')

@bp.route('/finished/')
def finished():
	return send_file('help/static/finished.html')

@bp.route('/process-feedback/')
def process():
	return send_file('help/static/process-feedback.html')

@bp.route('/delete-a-list/')
def delete_a_list():
	return send_file('help/static/delete-a-list.html')

@bp.route('/sign-into-your-account/')
def sign_into_your_account():
	return send_file('help/static/sign-into-your-account.html')

@bp.route('/reset-your-password/')
def reset_your_password():
	return send_file('help/static/reset-your-password.html')

