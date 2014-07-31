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
# 	name		{String}
# 	phonenumber	{String}
# 	location	{String}
# 	rooms 		[{ObjectId}] - array of ObjectId's
#	notes		{String}
#	price		{Integer} -- Integer not enforced server side
#	receipts 	[{ObjectId}] - array of ObjectId's of receipts
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from app.database import db
from .model_utility import stamp_last_modified, sanitize_id, sanitize_data
import room
import receipt
import cleaner

MUTABLE_FIELDS = ['name', 'phonenumber', 'location', 'notes', 'price',]
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



def find(id=None, _cleaner=None, populate_rooms=False, populate_cleaner=False):
	""" TODO: populate_rooms has no test coverage """
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	elif _cleaner:
		query['_cleaner'] = sanitize_id(_cleaner)
	lists = [l for l in db.lists.find(query)]

	if populate_rooms:
		for l in lists:
			l['rooms'] = room.find(_list=l['_id'], populate_tasks=True)

	if populate_cleaner:
		for l in lists:
			l['cleaner'] = cleaner.find_public(id=l['_cleaner'])
	return lists

def find_one(**kwargs):
	""" No test coverage TODO """
	l = find(**kwargs)
	return l[0] if l else None


def insert_new(cleaner_id, data=None):
	"""
	@param {ObjectId} cleaner_id
	Returns _id of newly inserted list 
	"""
	data = sanitize_data(data) if data else {}
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
	data = sanitize_data(data)
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


def create_receipt(list_id):
	"""
	@param {ObjectId} _id of list with which to make snapshot

	1) Retrieve fully populated list object 
	2) Create/insert receipt as snapshot of list 
	3) Add newly inserted receipt's _id to receipts list 

	Returns _id of newly inserted receipt
	"""
	list_id = sanitize_id(list_id)
	l = find_one(id=list_id, populate_rooms=True)
	if not l:
		raise Exception('Could not find list with id ' + list_id + ' when trying to create receipt')

	receipt_id = receipt.create(l)
	ret = db.lists.update({ "_id": list_id }, { "$push": {"receipts": receipt_id }})
	return receipt_id


def delete(id):
	"""
	1) notify all receipts of deletion
	2) delete all list's room documents
	3) delete cleaner's reference to list 
	4) delete list document
	"""
	id = sanitize_id(id)

	# 0) get list so have its _cleaner, rooms, and receipts _ids
	l = db.lists.find_one({ "_id": id })
	if not l:
		raise Exception("Cannot delete list with _id {0} - no such document".format(id))
	
	# 1)
	db.receipts.update({ "_list": id }, { "$set": {"_list": None }})

	# 2) delete all its rooms
	db.rooms.remove({ "_list": id })
	
	# 3) delete _cleaner's reference to it
	ret = db.cleaners.update({ "_id": sanitize_id(l["_cleaner"]) }, { "$pull": { "lists": id }})
	
	# 4) delete list document
	db.lists.remove({ "_id": id })






