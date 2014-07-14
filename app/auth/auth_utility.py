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
# 	/auth/auth_utility.py
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from flask import session

from app.lib.util import encoder


#- Session interactions ---------------------------------

def get_user():
	return session['user'] if 'user' in session else None

def logout():
	session['user'] = None

def login(user_data):
	user_data = encoder.encode(user_data)
	session['user'] = user_data

#--------------------------------- Session interactions -









