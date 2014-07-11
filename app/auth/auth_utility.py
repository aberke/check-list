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


#- Session interactions ---------------------------------

def get_user():
	return session['user'] if 'user' in session else None

def logout():
	session['user'] = None

def login(user_data):
	session['user'] = user_data

#--------------------------------- Session interactions -









