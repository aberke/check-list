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



def find(id=None, _list=None):
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	if _list:
		query['_list'] = sanitize_id(_list)
	feedbacks = [f for f in db.feedbacks.find(query)]
	return feedbacks


def find_one(**kwargs):
	f = find(**kwargs)
	return r[f] if r else None


def insert_new(list_id, data):
	"""
	@param {ObjectId} list_id
	Returns _id of newly inserted feedback
	"""
	data['_list'] = list_id
	# add date
	data['date'] = date_now()
	
	# insert into database
	feedback_id = db.feedbacks.insert(data)
	return feedback_id


def delete(id):
	"""
	1) delete _list's reference to feedback
	2) delete feedback document itself
	"""
	id = sanitize_id(id)
	# 0) get feedback document to have reference it its _list
	f = db.feedbacks.find_one({ "_id": id })
	if not f:
		raise Exception("Cannot delete feedback with _id {0} - no such document".format(id))
	# 1) delete _list's reference to it
	db.lists.update({ "_id": f["_list"] }, { "$pull": { "feedbacks": id }})
	
	# 2) delete feedback document
	db.feedbacks.remove({ "_id": id })