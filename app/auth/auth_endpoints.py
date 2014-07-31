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
# 	/auth/endpoints.py
#
#
# endpoints
# ------------------
# GET 		/auth/user			-> return current-user
# POST 		/auth/login 	-> login(user)
# POST,GET	/auth/logout 	-> logout(user)
# POST,PUT 	/auth/send-reset-code
# POST,PUT 	/auth/reset-password
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from flask import Blueprint, request, redirect
import json
from datetime import datetime

from app.lib import twilio_tools
from app.lib.util import yellERROR, dumpJSON, respond500, respond200, APIexception
from app.models import cleaner
from .auth_utility import *



bp = Blueprint('auth', __name__)


# - Auth routes ------------------------------------------

@bp.route('/send-reset-code', methods=['POST', 'PUT'])
def send_reset_code():
	"""
	Send reset_code via SMS to the user 
		Each reset_code expires after RESET_CODE_EXPIRATION
		If not yet set, or if expired, reset reset_code and reset_code_expires
	"""
	try:
		data = json.loads(request.data)
		if not 'phonenumber' in data:
			raise APIexception(code=1)
		
		phonenumber = data['phonenumber']
		c = cleaner.find_one(phonenumber=phonenumber)
		if not c:
			raise APIexception(code=2)

		if ('reset_code' in c and 'reset_code_expires' in c and (datetime.now() < c['reset_code_expires'])):
			reset_code = c["reset_code"]
		else:
			(reset_code, reset_code_expires) = cleaner.generate_reset_code()
			cleaner.update(c["_id"], {"reset_code": reset_code, "reset_code_expires": reset_code_expires})

		twilio_tools.send_SMS(phonenumber, str("Your password reset code is: " + reset_code))
		return respond200()
	except Exception as e:
		return respond500(e)

@bp.route('/reset-password', methods=['POST', 'PUT'])
def POST_reset_password():
	try:
		data = json.loads(request.data)
		c = cleaner.find_one(phonenumber=data['phonenumber'])
		if not (c and 'reset_code' in c):
			raise APIexception(code=0)

		if not ((data['reset_code'] == c["reset_code"]) and (datetime.now() < c['reset_code_expires'])):
			raise APIexception(code=3)

		# if they made it this far all is good
		cleaner.update_password(c["_id"], data["password"], c["salt"])

		login(cleaner.public(c))
		return respond200()
	except Exception as e:
		return respond500(e)



@bp.route('/user', methods=['GET'])
def GET_user():
	return dumpJSON(get_user())

@bp.route('/logout', methods=['POST'])
def HTTP_logout():
	""" Import that logout performed with a POST due to mobile browsers' aggressive caching """
	logout()
	return respond200() # dont redirect -- then caches will remember where to redirect to rather than making POST

@bp.route('/login', methods=['POST'])
def POST_login():
	try:
		data = json.loads(request.data)
		if not ("phonenumber" in data and "password" in data): # client-side shouldn't have allowed post
			raise APIexception(code=0, message="phonenumber and password required to sign in")

		c = cleaner.find_one(phonenumber=data["phonenumber"])
		if not c:
			raise APIexception(code=2)

		if not cleaner.password_valid(data["password"], c["salt"], c["hashed_pwd"]):
			raise APIexception(code=4)

		profile = cleaner.public(c)
		login(profile)
		return dumpJSON(profile)

	except Exception as e:
		return respond500(e)

# ------------------------------------------------------- Auth routes -
