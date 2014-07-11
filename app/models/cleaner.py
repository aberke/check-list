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
#
# Cleaner is the user model. Has
# 	phonenumber (unique)
# 		hashed_pwd	
# 		salt
# 		reset_code (temp code texted to user to reset password)
# 		reset_code_expires (datetime at which reset_code no longer valid)

# 	name
# 	lists [{ObjectId}] - array of ObjectId's
#
# TODO - TO PONDER
# 	collapse find_all and find into one?
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from bson import ObjectId

from app.database import db
from app import auth
from . import stamp_last_modified
import list




def find(id=None, phonenumber=None):
	query = {}
	if id:
		query['_id'] = ObjectId(id)
	elif phonenumber:
		query['phonenumber'] = phonenumber
	return [c for c in db.cleaners.find(query)]

def find_one(id=None, phonenumber=None):
	c = find(id=id, phonenumber=phonenumber)
	return c[0] if c else None

def find_public(id=None, phonenumber=None):
	return public(find_one(id, phonenumber))

def insert_new(data):
	if not ('phonenumber' in data and data['password']):
		raise Exception('new cleaner data must include phonenumber and password')

	if db.cleaners.find_one({"phonenumber": data["phonenumber"]}):
		raise Exception("cleaner with phonenumber {0} already exists".format(data["phonenumber"]))

	salt = auth.generate_salt()
	hashed_pwd = auth.hash_password(data["password"], salt)

	data = stamp_last_modified({
		"name": data["name"],
		"phonenumber": data['phonenumber'],
		"salt": salt,
		"hashed_pwd": hashed_pwd,
		"lists": [], # list of _ids of documents in the lists collection
	})
	ret = db.cleaners.insert(data)
	return ret

def update(id, data):
	# TODO - RAISE ERROR for unsatisfactory write result ?
	data = stamp_last_modified(data)
	ret = db.cleaners.update({ "_id": ObjectId(id) }, { "$set": data})
	return ret

def add_list(cleaner_id, list_data=None):
	cleaner_id = ObjectId(cleaner_id)
	list_id = list.insert_new(cleaner_id, list_data)
	ret = db.cleaners.update({ "_id": cleaner_id }, { "$push": {"lists": list_id }})
	return list_id

def public(cleaner):
	if not cleaner:
		return None
	exclude_fields = ['salt', 'hashed_pwd']
	profile = {}
	for (key, value) in cleaner.items():
		if key in exclude_fields:
			continue
		if isinstance(value, ObjectId):
			value = str(value)
		profile[key] = value

	return profile





















