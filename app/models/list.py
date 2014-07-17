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
# List Model
# 	_id 		{ObjectId}
# 	_cleaner  	{ObjectId}	-- cleaner._id of owner cleaner
# 	name
# 	phonenumber
# 	location
# 	rooms 		[{ObjectId}] - array of ObjectId's
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from app.database import db
from .model_utility import stamp_last_modified, sanitize_id
import room

MUTABLE_FIELDS = ['name', 'phonenumber', 'location']
DEFAULT_ROOMS = [{
		'name': 'BATHROOM',
		'type': 'bathroom',
		'tasks': [],
	},{
		'name': 'KITCHEN',
		'type': 'kitchen',
		'tasks': [],
	},{
		'name': 'BEDROOM',
		'type': 'bedroom',
		'tasks': [],
	},{
		'name': 'LIVING ROOM',
		'type': 'living-room',
		'tasks': [],
	},]



def find(id=None, _cleaner=None):
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	elif _cleaner:
		query['_cleaner'] = sanitize_id(_cleaner)
	result = [l for l in db.lists.find(query)]
	return result


def insert_new(cleaner_id, data=None):
	"""
	@param {ObjectId} cleaner_id
	Returns _id of newly inserted list 
	"""
	data = data if data else {}
	data["_cleaner"] = cleaner_id
	data["rooms"] = []
	data = stamp_last_modified(data)
	list_id = db.lists.insert(data)

	# TODO - BETTER SOLUTION
	for room in DEFAULT_ROOMS:
		add_room(list_id, room.copy())

	return list_id


def update(id, data):
	"""
	Only allowed to update list info 
	"""
	data = {k:v for (k,v) in data.items() if k in MUTABLE_FIELDS}

	# TODO - RAISE ERROR for unsatisfactory write result ?
	data = stamp_last_modified(data)
	ret = db.lists.update({ "_id": sanitize_id(id) }, { "$set": data})
	return ret


def add_room(list_id, room_data=None):
	room_data = room_data if room_data else {}
	list_id = sanitize_id(list_id)
	room_data['_list'] = list_id
	room_id = room.insert_new(list_id, room_data)
	ret = db.lists.update({ "_id": list_id }, { "$push": {"rooms": room_id }})
	return room_id

def delete(id):
	"""
	1) delete all list's room documents
	2) delete cleaner's reference to list 
	3) delete list document
	"""
	id = sanitize_id(id)
	# 0) get list so have its _cleaner and rooms _ids
	l = db.lists.find_one({ "_id": id })
	if not l:
		raise Exception("Cannot delete list with _id {0} - no such document".format(id))
	
	# 1) delete all its rooms
	db.rooms.remove({ "_list": id })
	
	# 2) delete _cleaner's reference to it
	ret = db.cleaners.update({ "_id": sanitize_id(l["_cleaner"]) }, { "$pull": { "lists": id }})
	
	# 3) delete list document
	db.lists.remove({ "_id": id })






