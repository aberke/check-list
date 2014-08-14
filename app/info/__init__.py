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
#	Base file of info module
# 	/info/__init__.py
#
# 	Static files created by Sean Nurse (Designer Intern)
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, send_file



bp = Blueprint('info', __name__, static_url_path='', static_folder='static')


@bp.route('/')
def info():
	return send_file('info/static/index.html')