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
# Room Model
# 	_id		{ObjectId}
# 	_list 	{ObjectId}		<- list._id of owner list
# 	name	{String}
# 	type 	{String}		<- icon etc
# 	tasks 	{array}
#	count
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from app.database import db
from .model_utility import stamp_last_modified, sanitize_id
import task


MUTABLE_FIELDS = ['name', 'type', 'count']


def find(id=None, _list=None, populate_tasks=False):
	"""
	By default returns all specified rooms with tasks list of task._id's 
	If with_tasks==True: Populates tasks 
	"""
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	if _list:
		query['_list'] = sanitize_id(_list)

	rooms = [r for r in db.rooms.find(query)]

	if populate_tasks:
		for r in rooms:
			r['tasks'] = task.find(_room=r['_id'])

	return rooms

def find_one(**kwargs):
	result = find(**kwargs)
	return result[0] if result else None

def insert_new(list_id, data=None):
	"""
	@param {ObjectId} list_id
	Returns _id of newly inserted room 
	"""
	data = data if data else {}
	data["_list"] = list_id
	data["tasks"] = []
	data = stamp_last_modified(data)
	return db.rooms.insert(data)

def update(id, data):
	# TODO - RAISE ERROR for unsatisfactory write result ?
	data = {k:v for (k,v) in data.items() if k in MUTABLE_FIELDS}
	data = stamp_last_modified(data)
	ret = db.rooms.update({ "_id": sanitize_id(id) }, { "$set": data})
	return ret

def add_task(room_id, task_data):
	room_id = sanitize_id(room_id)
	task_id = task.insert_new(room_id, task_data)
	ret = db.rooms.update({ "_id": room_id }, { "$push": {"tasks": task_id }})
	return task_id

def delete(id):
	"""
	1) delete _list's reference to room
	2) delete room document itself
	"""
	id = sanitize_id(id)
	# 0) get room document to have reference it its _list
	r = db.rooms.find_one({ "_id": id })
	if not r:
		raise Exception("Cannot delete room with _id {0} - no such document".format(id))
	# 1) delete _list's reference to it
	db.lists.update({ "_id": r["_list"] }, { "$pull": { "rooms": id }})
	
	# 2) delete room document
	db.rooms.remove({ "_id": sanitize_id(id) })
	


