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
#
#	util file
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Response
import json
from bson import ObjectId
from datetime import datetime

import error_codes




from functools import wraps
from flask import request, current_app
def jsonp(func):
    """
    Taken from:  https://gist.github.com/1094140
    Wraps JSONified output for JSONP requests.
    """
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


class JSONEncoder(json.JSONEncoder):
	# Custom JSONJSONencoder because by default, json cannot handle datetimes or ObjectIds """
	def default(self, o):
		if isinstance(o, datetime):
			return str(o)
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)

	def decode(self, data):
		if not type(data) == dict:
			return data
		if '_id' in data:
			data['_id'] = ObjectId(data['_id'])
		if '_cleaner' in data:
			data['_cleaner'] = ObjectId(data['_cleaner'])
		if '_list' in data:
			data['_list'] = ObjectId(data['_list'])
		if '_room' in data:
			data['_room'] = ObjectId(data['_room'])
		return data

	def load(self, data):
		if not data:
			return None
		return self.decode(json.loads(data))


JSONencoder = JSONEncoder()


class APIexception(Exception):
	code = 0
	message = None
	original_message = None

	def yell(self, message):
		print("\n************ ERROR **************\n" + str(message) + "\n************* ERROR *************\n")

	def __init__(self, message='', code=0):
		if not code in error_codes.map:
			self.yell('Invalid error code: ' + str(code))
			code = 0

		self.code = code
		self.original_message = message
		self.message = error_codes.map[code]
		Exception.__init__(self, message)
		yellERROR("Original message: {0}\nMessage: {1}".format(self.original_message, self.message)) # yell the error for logs


def respond500(exception):
	"""
	@param {int} code: error code for which to find error string in error_codes map
	@param {str} err: optional error message to YELL to server for logs
	
	Philosophy:
	Return a small set of error strings 
		- These strings are keywords in the translations spreadsheet that have translations
	Use:
	When endpoints are hit with bad data or cause accidental exceptions to occur
	It catches accidentally raised Exceptions 
		- In this case, expects code==0
		- Returns nicely formatted response to user rather than cryptic mongo/python error 
	It it called directly when endpoint receives invalid data 
		- Expects code in error_codes map
	"""
	if not isinstance(exception, APIexception):
		exception = APIexception(message=exception.message)

	data = json.dumps({ 'message': exception.message, 'code': exception.code })
	response_headers = {'Content-Type': 'application/json'}
	return Response(data, 500, response_headers)


def respond200():
	return Response(status=200)


def dumpJSON(data):
	if not isinstance(data, str):
		data = JSONencoder.encode(data)
	response_headers = {'Content-Type': 'application/json'}
	return Response(data, 200, response_headers)



def yellERROR(msg=None):
	print("\n************ ERROR **************\n" + str(msg) + "\n************* ERROR *************\n")