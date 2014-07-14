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
# Task Model
# 	_id		{ObjectId}
# 	_room 	{ObjectId}	<- room._id of owner room
# 	name
#
#--------------------------------------------------------------------------------
#*********************************************************************************


# TODO -- TEST

from bson import ObjectId

from app.database import db
from .model_utility import stamp_last_modified



def find(id=None, _room=None):
	query = {}
	if id:
		query['_id'] = ObjectId(id)
	elif _list:
		query['_room'] = ObjectId(_room)
	return [t for t in db.tasks.find(query)]

def insert_new(list_id, data):
	"""
	@param {ObjectId} room_id
	Returns _id of newly inserted task 
	"""
	if not ('name' in data and type(data)==dict):
		raise Exception('Tried to insert new task without a name')

	data["_room"] = list_id
	return db.tasks.insert(data)

	


