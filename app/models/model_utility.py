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
#********************************************************************************
#--------------------------------------------------------------------------------



from bson import ObjectId
from datetime import datetime 


def sanitize_phonenumber(phonenumber):
	""" All phonenumbers should be stored as strings """
	return str(phonenumber)


def sanitize_id(id):
	return ObjectId(id)

def sanitize_notes(notes):
	""" Mongo StringField size limit is 16MB per document - so string works for arbitrary text field """
	return str(notes)


def sanitize_data(data):
	"""
	Assert only certain types make it into database and are queried for 
	"""
	if '_id' in data:
		data['_id'] = ObjectId(data['_id'])
	if 'phonenumber' in data:
		data['phonenumber'] = sanitize_phonenumber(data['phonenumber'])
	if 'notes' in data:
		data['notes'] = sanitize_notes(data['notes'])
	return data


def date_now():
	return str(datetime.utcnow())


def stamp_last_modified(data):
	"""
	@param {dict} data  -- data with which to add key/value pair ('last_modified', UTC now date)
	Returns original data with extra key/value pair ('last_modified', UTC now date)
	
	cleaners, lists, and rooms collections all have a last_modified field 
	that should be updated with each insertion and update 
	"""
	data['last_modified'] = date_now()
	return data
