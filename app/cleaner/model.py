#********************************************************************************
#--------------------------------------------------------------------------------
#
#	Significance Labs
#	Brooklyn, NYC
#
# 	Author: Alexandra Berke (aberke)
# 	Written: June 2014
#
#
# 	cleaner model
#
#--------------------------------------------------------------------------------
#*********************************************************************************


"""
Cleaner is the user model. Has
	phonenumber (unique)
		hashed_pwd	
		salt
		reset_code (temp code texted to user to reset password)
		reset_code_expires (datetime at which reset_code no longer valid)

	name
"""

from bson import ObjectId

from ..database import db
import auth




def get_all():
	return db.cleaners.find()

def insert_new_cleaner(data):
	if not ('phonenumber' in data and data['password']):
		raise Exception('new cleaner data must include phonenumber and password')

	if db.cleaners.find_one({"phonenumber": data["phonenumber"]}):
		raise Exception("cleaner with phonenumber {0} already exists".format(data["phonenumber"]))

	salt = auth.generate_salt()
	hashed_pwd = auth.hash_password(data["password"], salt)

	ret = db.cleaners.insert({
		"name": data["name"],
		"phonenumber": data['phonenumber'],
		"salt": salt,
		"hashed_pwd": hashed_pwd,
	})
	return ret

def get_cleaner(id=None, phonenumber=None):
	cleaner = None
	if id:
		cleaner = db.cleaners.find_one({"_id": ObjectId(id)})
	elif phonenumber:
		cleaner = db.cleaners.find_one({"phonenumber": phonenumber})
	return cleaner

def update_cleaner(id, data):
	# TODO - RAISE ERROR for unsatisfactory write result ?
	ret = db.cleaners.update({ "_id": ObjectId(id) }, { "$set": data})
	return ret


def public_cleaner(cleaner):
	exclude_fields = ['salt', 'hashed_pwd']
	profile = {}
	for (key, value) in cleaner.items():
		if key in exclude_fields:
			continue
		if isinstance(value, ObjectId):
			value = str(value)
		profile[key] = value

	return profile




