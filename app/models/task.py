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
# 	name	{String}
#
#--------------------------------------------------------------------------------
#*********************************************************************************



from app.database import db
from .model_utility import stamp_last_modified, sanitize_id




def find(id=None, _room=None):
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	elif _room:
		query['_room'] = sanitize_id(_room)
	return [t for t in db.tasks.find(query)]

def insert_new(list_id, data):
	"""
	@param {ObjectId} room_id
	Returns _id of newly inserted task 
	"""
	if not (type(data)==dict and 'name' in data):
		raise Exception('Tried to insert new task without a name')

	data["_room"] = list_id
	return db.tasks.insert(data)

def delete(id):
	"""
	1) delete _room's reference to task
	2) delete task document itself
	"""
	id = sanitize_id(id)
	# 0) get task document to have reference it its _list
	t = db.tasks.find_one({ "_id": id })
	if not t:
		raise Exception("Cannot delete task with _id {0} - no such document".format(id))
	# 1) delete _room's reference to it
	db.rooms.update({ "_id": t["_room"] }, { "$pull": { "tasks": id }})
	
	# 2) delete task document
	db.tasks.remove({ "_id": id })
	


