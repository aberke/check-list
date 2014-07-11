#********************************************************************************
#--------------------------------------------------------------------------------
#
#	Significance Labs
#	Brooklyn, NYC
#
# 	Author: Alexandra Berke (aberke)
# 	Written: Summer 2014
#
#	DEPRECATED -- NOT IN USE
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request, session, redirect
import json


from app.lib.util import yellERROR, dumpJSON, respond500, respond200
from app.lib import twilio_tools, s3
import auth
import model


bp = Blueprint('cleaner', __name__)


"""
endpoints
------------------
GET 		/cleaner/all
POST 		/cleaner    			-> create user, login(user)
GET,PUT		/cleaner/<id>
POST 		/cleaner/<id>/booking 		
GET			/cleaner/lookup/phonenumber/<phonenumber>
GET 		/cleaner/validate-new-phonenumber/<phonenumber>

authentication endpoints via the auth Blueprint

"""

# -- API routes --------------------------------------------------------

@bp.route('/<id>', methods=['PUT'])
def PUT_profile(id):
	try:
		data = json.loads(request.data)
		# filter in only the data that is allowed for update
		filtered_keys = ["name", "blurb", "rates_text", "conditions_text", "services_text", "locations_text"]
		ret = model.update_cleaner(id, {k: data[k] for k in filtered_keys if k in data})
		return respond200()
	except Exception as e:
		return respond500(e)


@bp.route('', methods=['POST'])
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


@bp.route('/<id>/booking', methods=['POST'])
def POSTbooking(id):
	try:
		data = json.loads(request.data)
		booking = data['booking']
		cleaner = model.get_cleaner(id=id)
		twilio_tools.send_booking_confirmations(cleaner, booking)
		return respond200()
	except Exception as e:
		return respond500(e)


@bp.route('/all', methods=['GET'])
def GET_all_cleaners():
	try:
		cleaners = model.get_all()
		return dumpJSON([c for c in cleaners])
	except Exception as e:
		return respond500(e)


@bp.route('/<id>', methods=['GET'])
def GET_cleaner_by_id(id):
	try:
		cleaner = model.get_cleaner(id=id)
		return dumpJSON(cleaner)
	except Exception as e:
		return respond500(e)

@bp.route('/lookup/phonenumber/<phonenumber>')
def GET_cleaner_by_phonenumber(phonenumber):
	cleaner = model.get_cleaner(phonenumber=phonenumber)
	return dumpJSON(cleaner)

@bp.route('/validate-new-phonenumber/<phonenumber>')
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



















