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
# 	/auth/auth_core.py
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from flask import session

import hashlib, uuid # for passwords
import string
import random


#- Session interactions ---------------------------------
def get_user():
	return session['user'] if 'user' in session else None

def logout():
	session['user'] = None

def login(user_data):
	session['user'] = user_data

#--------------------------------- Session interactions -



#- Helper methods -----------------------------------

def generate_salt():
	return uuid.uuid4().hex

def hash_password(password, salt):
	return hashlib.sha512(password + salt).hexdigest()

def password_valid(password, salt, hashed_pwd):
	hash = hash_password(password, salt)
	return (hashed_pwd == hash)

def code_generator(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

#----------------------------------- Helper methods -







