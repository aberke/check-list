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
# 	phonenumber 			{string} (unique)
# 		hashed_pwd			{string}
# 		salt 				{string}
# 		reset_code 			{string} (temp code texted to user to reset password)
# 		reset_code_expires  {string} (datetime at which reset_code no longer valid)

# 	name 					{string}
# 	lists 					[{ObjectId}] - array of ObjectId's
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from bson import ObjectId
import hashlib, uuid # for passwords
# for reset_code
import string, random
from datetime import datetime, timedelta 

from app.database import db
from .model_utility import stamp_last_modified, sanitize_data, sanitize_phonenumber, sanitize_id
import list

RESET_CODE_EXPIRATION = timedelta(hours=1)
MUTABLE_FIELDS = ['name', 'phonenumber', 'salt', 'hashed_pwd', 'reset_code', 'reset_code_expires']



def find(id=None, phonenumber=None):
	query = {}
	if id:
		query['_id'] = sanitize_id(id)
	if phonenumber:
		query['phonenumber'] = sanitize_phonenumber(phonenumber)
	return [c for c in db.cleaners.find(query)]


def find_one(**kwargs):
	c = find(**kwargs)
	return c[0] if c else None


def find_public(**kwargs):
	return public(find_one(**kwargs))


def insert_new(data):
	data = sanitize_data(data)
	if not ('phonenumber' in data and data['password']):
		raise Exception('new cleaner data must include phonenumber and password')

	if db.cleaners.find_one({"phonenumber": data["phonenumber"]}):
		raise Exception("cleaner with phonenumber {0} already exists".format(data["phonenumber"]))

	salt = generate_salt()
	hashed_pwd = hash_password(data["password"], salt)

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
	data = {k:v for (k,v) in data.items() if k in MUTABLE_FIELDS}
	data = sanitize_data(data)
	data = stamp_last_modified(data)
	ret = db.cleaners.update({ "_id": sanitize_id(id) }, { "$set": data})
	return ret

def update_password(id, new_password, salt):
	new_hashed_pwd = hash_password(new_password, salt)
	update(id, { "hashed_pwd": new_hashed_pwd })

def add_list(cleaner_id, list_data=None):
	cleaner_id = sanitize_id(cleaner_id)
	list_id = list.insert_new(cleaner_id, data=list_data)
	ret = db.cleaners.update({ "_id": cleaner_id }, { "$push": {"lists": list_id }})

	print('**************---------------')
	print('cleaner_id', cleaner_id)
	print('list_id', list_id)
	print('add_list ret:', ret)
	print('**************---------------')

	# Potential bad situation: Cleaner deleted but user still logged in as cleaner and able to make posts to add list
	# avoid this situation by ensuring that 1 cleaner matched list._cleaner
	# if error occurs, delete the newly inserted list - it should never have been created
	if ret['nModified'] != 1:
		list.delete(list_id)
		raise Exception("Error when trying to add list to cleaner {0}: {1} cleaners updated".format(cleaner_id, ret['nModified']))
	
	return list_id

def public(cleaner):
	if not (cleaner and cleaner['_id']):
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


def delete(id):
	"""
	1) delete all lists belonging to cleaner - delete will travel recursively: lists will handle deleting receipts, and rooms, etc
	2) delete cleaner document itself
	"""
	id = sanitize_id(id)

	# 0) get cleaner so have its lists
	c = db.cleaners.find_one({ "_id": id })
	if not c:
		raise Exception("Cannot delete cleaner with _id {0} - no such document".format(id))
	
	# 1) delete all lists belonging to it
	for l in c['lists']:
		list.delete(l)
	
	# 2) delete document itself
	db.cleaners.remove({ "_id": id })






#- Helper methods -----------------------------------

def generate_salt():
	return uuid.uuid4().hex

def hash_password(password, salt):
	return hashlib.sha512(password + salt).hexdigest()

def password_valid(password, salt, hashed_pwd):
	""" Returns true if the supplied password/salt combination matches hashed password """
	hash = hash_password(password, salt)
	return (hashed_pwd == hash)

def code_generator(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_reset_code():	
	reset_code = code_generator(size=4)
	reset_code_expires = datetime.now() + RESET_CODE_EXPIRATION
	return (reset_code, reset_code_expires)

#----------------------------------- Helper methods -
















