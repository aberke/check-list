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
	# Custom JSONEncoder because by default, json cannot handle datetimes or ObjectIds """
    def default(self, o):
		if isinstance(o, datetime):
			return str(o)
		if isinstance(o, ObjectId):
		    return str(o)
		return json.JSONEncoder.default(self, o)

encoder = JSONEncoder()


def dumpJSON(data, mongo=False):
	if not isinstance(data, str):
		data = encoder.encode(data)
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