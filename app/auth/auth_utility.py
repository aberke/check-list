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

from app.lib.util import JSONencoder
from app.models import cleaner


#- Session interactions ---------------------------------

def get_user():
	"""
	Returns JSON encoded user if user in session, otherwise None

	** Potential issue I want to avoid:
		cleaner (user) was deleted (via backstage or direct database interaction) or something else bazaar happened
		yet cleaner is somehow still in session
		If this occurs - take user out of session
	"""
	if not ('user' in session and session['user']):
		return None

	# **see note above
	user = JSONencoder.load(session['user'])
	if not cleaner.find_one(id=user['_id']):
		session['user'] = None

	return session['user']


def logout():
	session['user'] = None

def login(user_data):
	user_data = JSONencoder.encode(user_data)
	session['user'] = user_data

#--------------------------------- Session interactions -









