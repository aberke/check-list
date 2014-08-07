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
# 	Receipt Model
#		a receipt is a static snapshot of a list at a given time
#		it has a date (when created/sent to client)
#		instead of referring to specific room and task models, it stores all data as embedded documents
#			since this data cannot change
#
#	Lists may be deleted, but receipts live forever
#		When a list is deleted, instead of deleting receipt,
#		receipt updated such that _list=null
#
#
# 	_id 		{ObjectId}
# 	_cleaner  	{ObjectId}	-- cleaner._id of owner cleaner
# 	_list		{ObjectId}	-- list._id of owner list -- set to null when list deleted
# 	date 		{Date}		-- set at time of creation
#	phonenumber	{String}
# 	location	{String}
#	notes		{String}
#	price		{Integer} -- Integer not enforced server side
# 	rooms 		[{
# 					name	{String}
# 					type 	{String}		<- icon etc
#					count	{Number} 		<- front end defaults to 1 if not set
# 					tasks 	[{
#								name	{String}
#							},{
#							...
#							}]
#				},{
#				...
#				}]
#
#--------------------------------------------------------------------------------
#*********************************************************************************

import copy
from datetime import datetime 

from app.database import db 
from .model_utility import sanitize_id
import cleaner



def find(id=None):
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	receipts = [r for r in db.receipts.find(query)]
	for r in receipts:
		r['cleaner'] = cleaner.find_public(id=r['_cleaner'])
	return receipts

def find_one(**kwargs):
	r = find(**kwargs)
	return r[0] if r else None

def mark_list_deleted(id):
	"""
	NOT USED
	When a list is deleted, instead of deleting receipt, it notifies receipt 
	Receipt then updates _list to be null
	"""
	return db.receipts.update({ "_id": sanitize_id(id) }, { "$set": {"_list": None }})


def create(list):
	"""
	This method should only be called from list.create_receipt

	@param {dict} list model object fully populated with rooms that are fully populated with tasks
	Returns _id of newly inserted receipt

	Takes snapshot of list and creates receipt
	"""
	receipt_data = copy.deepcopy(list)
	del receipt_data['_id']
	del receipt_data['last_modified']
	receipt_data['_list'] = sanitize_id(list['_id'])
	# add date
	receipt_data['date'] = str(datetime.utcnow())
	
	# insert into database
	receipt_id = db.receipts.insert(receipt_data)
	return receipt_id