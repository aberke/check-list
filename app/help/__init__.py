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
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, send_file



bp = Blueprint('help', __name__, static_folder='static')


@bp.route('/')
def index():
	return send_file('help/static/index.html')