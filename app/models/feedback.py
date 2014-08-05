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
#	feedback model
#
# 	_id 		{ObjectId}
# 	_list		{ObjectId}	-- list._id of owner list
# 	_receipt	{ObjectId}	-- receipt._id of receipt posted from
# 	date 		{Date}		-- set at time of creation
#	rating		{Number}
#	why			{String}
# 	request 	{String}
#
#--------------------------------------------------------------------------------
#*********************************************************************************

import copy
from datetime import datetime 

from app.database import db 
from .model_utility import sanitize_id, date_now
import list
import receipt



def find(id=None):
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	feedbacks = [f for f in db.receipts.find(query)]
	return feedbacks

def find_one(**kwargs):
	f = find(**kwargs)
	return r[f] if r else None

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

def create(list_id, data):
	"""
	@param {ObjectId} list_id
	Returns _id of newly inserted feedback
	"""
	data['_list'] = list_id
	# add date
	data['date'] = date_now()
	
	# insert into database
	feedback_id = db.feedbackss.insert(data)
	return feedback_id

