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


def dumpJSON(data):
	if not isinstance(data, str):
		data = JSONencoder.encode(data)
	response_headers = {'Content-Type': 'application/json'}
	return Response(data, 200, response_headers)


def respond200():
	return Response(status=200)


def respond500(code=0, err='ERROR'):
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
	try:
		message = error_codes.map[code]
		yellERROR("Original message: {0}\nReturned message: {1}".format(err, message)) # yell the error for logs
	except Exception as e:
		yellERROR('INCORRECT USE OF respond500\nOriginal err: {0}'.format(err))
		message = error_codes.map[0]

	data = json.dumps({ 'message': message, 'code': code })
	response_headers = {'Content-Type': 'application/json'}
	return Response(data, 500, response_headers)


def yellERROR(msg=None):
	print("\n************ ERROR **************\n" + str(msg) + "\n************* ERROR *************\n")