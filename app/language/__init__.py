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
#	Base file of language module
# 	/language/__init__.py
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request

from app.lib.util import dumpJSON, respond500, respond200
from map import get_map

"""
Taken from:  https://gist.github.com/1094140
"""

from functools import wraps
from flask import request, current_app


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function

bp = Blueprint('language', __name__, static_folder='static')



@bp.route('/')
def view():

	return 'language'

@bp.route('/map')
@jsonp
def map():
	try:
		data = get_map()
		return dumpJSON(data)
	except Exception as e:
		return respond500(e)


























