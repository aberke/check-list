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
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request, session, redirect
import json

from ..util import yellERROR, dumpJSON, respond500, respond200
import app.twilio_tools as twilio_tools
import app.s3 as s3
import auth
import model


cleaner = Blueprint('cleaner', __name__)


"""
endpoints
------------------
POST 		/cleaner    			-> create user, login(user)
GET 		/cleaner/all
GET			/cleaner/<id>
PUT 	 	/cleaner/<id>
POST 		/cleaner/<id>/booking 		
GET			/cleaner/lookup/phonenumber/<phonenumber>

GET 		/cleaner/auth 			-> return current-user
POST 		/cleaner/auth/login 	-> login(user)
POST,GET	/cleaner/auth/logout 	-> logout(user)
POST,PUT 	/cleaner/auth/send-reset-code
POST,PUT 	/cleaner/auth/reset-password

"""

# -- API routes --------------------------------------------------------

@cleaner.route('/<id>', methods=['PUT'])
def PUT_profile(id):
	try:
		data = json.loads(request.data)
		# filter in only the data that is allowed for update
		filtered_keys = ["name", "blurb", "rates_text", "conditions_text", "services_text", "locations_text"]
		ret = model.update_cleaner(id, {k: data[k] for k in filtered_keys if k in data})
		return respond200()
	except Exception as e:
		return respond500(e)


@cleaner.route('', methods=['POST'])
def POST_profile():
	""" Insert and login new cleaner """
	try:
		data = json.loads(request.data)
		id = model.insert_new_cleaner(data)
		cleaner = model.get_cleaner(id=id)
		profile = model.public_cleaner(cleaner)
		auth.login(profile)
		return dumpJSON(profile)
	except Exception as e:
		return respond500(e)


@cleaner.route('/<id>/booking', methods=['POST'])
def POSTbooking(id):
	try:
		data = json.loads(request.data)
		booking = data['booking']
		cleaner = model.get_cleaner(id=id)
		twilio_tools.send_booking_confirmations(cleaner, booking)
		return respond200()
	except Exception as e:
		return respond500(e)


@cleaner.route('/all', methods=['GET'])
def GET_all_cleaners():
	try:
		cleaners = model.get_all()
		return dumpJSON([c for c in cleaners])
	except Exception as e:
		return respond500(e)


@cleaner.route('/<id>', methods=['GET'])
def GET_cleaner_by_id(id):
	try:
		cleaner = model.get_cleaner(id=id)
		return dumpJSON(cleaner)
	except Exception as e:
		return respond500(e)

@cleaner.route('/lookup/phonenumber/<phonenumber>')
def GET_cleaner_by_phonenumber(phonenumber):
	cleaner = model.get_cleaner(phonenumber=phonenumber)
	return dumpJSON(cleaner)

@cleaner.route('/validate-new-phonenumber/<phonenumber>')
def GET_validate_new_phonenumber(phonenumber):
	cleaner = model.get_cleaner(phonenumber=phonenumber)
	if cleaner:
		return respond500(str("User with phone number " + phonenumber + " already exists"))
	try:
		twilio_tools.send_SMS(phonenumber, "Welcome to Clean Slate!")
		return respond200()
	except Exception as e:
		return respond500(e)

# ------------------------------------------------------- API routes -



# - Auth routes ------------------------------------------

from datetime import datetime, timedelta
RESET_CODE_EXPIRATION = timedelta(hours=1)

@cleaner.route('/auth/send-reset-code', methods=['POST', 'PUT'])
def send_reset_code():
	"""
	Send reset_code via SMS to the user 
		Each reset_code expires after RESET_CODE_EXPIRATION
		If not yet set, or if expired, reset reset_code and reset_code_expires
	"""
	try:
		data = json.loads(request.data)
		if not 'phonenumber' in data:
			raise Exception("No phonenumber provided")
		phonenumber = data['phonenumber']
		cleaner = model.get_cleaner(phonenumber=phonenumber)
		if not cleaner:
			raise Exception(str("No user with phonenumber " + phonenumber))

		if ('reset_code' in cleaner and 'reset_code_expires' in cleaner and (datetime.now() < cleaner['reset_code_expires'])):
			reset_code = cleaner["reset_code"]
		else:
			reset_code = auth.code_generator(size=4)
			reset_code_expires = datetime.now() + RESET_CODE_EXPIRATION
			model.update_cleaner(cleaner["_id"], {"reset_code": reset_code, "reset_code_expires": reset_code_expires})

		twilio_tools.send_SMS(phonenumber, str("Your password reset code is: " + reset_code))
		return respond200()
	except Exception as e:
		return respond500(e)

@cleaner.route('/auth/reset-password', methods=['POST', 'PUT'])
def POST_reset_password():
	try:
		data = json.loads(request.data)
		cleaner = model.get_cleaner(phonenumber=data["phonenumber"])
		if not (cleaner and 'reset_code' in cleaner):
			raise Exception(str("Something went wrong"))

		if not ((data['reset_code'] == cleaner["reset_code"]) and (datetime.now() < cleaner['reset_code_expires'])):
			raise Exception(str("Invalid password reset code"))

		# if they made it this far all is good
		new_hashed_pwd = auth.hash_password(data["password"], cleaner["salt"])
		model.update_cleaner(cleaner["_id"], {"hashed_pwd": new_hashed_pwd})

		cleaner_data = model.public_cleaner(cleaner)
		auth.login(cleaner_data)
		return respond200()
	except Exception as e:
		return respond500(e)



@cleaner.route('/auth', methods=['GET'])
def GET_user():
	return dumpJSON(auth.get_user())

@cleaner.route('/auth/logout', methods=['GET', 'POST'])
def logout():
	auth.logout()
	return redirect('/')

@cleaner.route('/auth/login', methods=['POST'])
def POST_login(data=None):
	try:
		data = json.loads(request.data)
		if not (data["phonenumber"] and data["password"]):
			raise Exception("phonenumber and password required to log in")

		cleaner = model.get_cleaner(phonenumber=data['phonenumber'])
		if not cleaner:
			raise Exception("No cleaner with phonenumber {0}".format(data["phonenumber"]))

		if not auth.password_valid(data["password"], cleaner["salt"], cleaner["hashed_pwd"]):
			raise Exception("Incorrect password")

		profile = model.public_cleaner(cleaner)
		auth.login(profile)
		return dumpJSON(profile)

	except Exception as e:
		return respond500(e)

# ------------------------------------------------------- Auth routes -

















