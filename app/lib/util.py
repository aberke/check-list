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

def respond500(err='ERROR'):
	yellERROR(err)
	data = json.dumps({'message': str(err)})
	response_headers = {'Content-Type': 'application/json'}
	return Response(data, 500, response_headers)

def respond200():
	return Response(status=200)

def yellERROR(msg=None):
	print("\n**************************\nERROR\n" + str(msg) + "\n**************************\n")