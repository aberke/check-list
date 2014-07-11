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
# 	api.py
# 	API endpoints
# 	-------------------------
# GET 				/api/cleaner/validate-new-phonenumber/<phonenumber>
# POST 				/api/cleaner
# GET 				/api/cleaner/search ?phonenumber=phonenumber || returns all
# GET,PUT 			/api/cleaner/<id>
# POST 				/api/cleaner/<id>/list
#
# GET 				/api/list/search ?_cleaner=cleaner._id | returns all
# GET,PUT,DELETE 	/api/list/<id>
# POST,PUT 			/api/list/<id>/send
# POST 				/api/list/<id>/room
#
# GET 				/api/room/search ?_list=list._id | returns all
# GET,PUT,DELETE 	/api/room/<id>
# POST,PUT 			/api/room/<id>/task
#
# TODO:
# TEST ALL ENDPOINTS
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request, session, redirect
import json


from app.lib.util import yellERROR, dumpJSON, respond500, respond200
from app.lib import twilio_tools, s3
from app import auth
from app.models import cleaner, list as List, room



bp = Blueprint('api', __name__)



#POST 		/api/cleaner
@bp.route('/cleaner', methods=['POST'])
def POST_cleaner():
	""" Insert and login new cleaner """
	try:
		data = json.loads(request.data)
		id = cleaner.insert_new(data)
		c = cleaner.find_public(id=id)
		auth.login(c)
		return dumpJSON(c)
	except Exception as e:
		return respond500(e)

# PUT 	/api/cleaner/<id>
@bp.route('/cleaner/<id>', methods=['PUT'])
def PUT_cleaner(id):
	try:
		data = json.loads(request.data)
		cleaner.update(id, data)
		return respond200()
	except Exception as e:
		return respond500(e)


#GET 		/api/cleaner/search
@bp.route('/cleaner/search', methods=['GET'])
def GET_cleaner_search():
	""" If phonenumber in request args, search by phonenumber, 
			else search for all 
		returns List

		TODO: return public result only?
	"""
	try:
		if 'phonenumber' in request.args:
			result = cleaner.find(phonenumber=request.args['phonenumber'])
		else:
			result = cleaner.find()
		return dumpJSON(result)
	except Exception as e:
		return respond500(e)

#GET 	/api/cleaner/<id>
@bp.route('/cleaner/<id>', methods=['GET'])
def GET_cleaner_by_id(id):
	try:
		return dumpJSON(cleaner.find_one(id=id))
	except Exception as e:
		return respond500(e)

# GET 		/api/cleaner/validate-new-phonenumber/<phonenumber>
@bp.route('/cleaner/validate-new-phonenumber/<phonenumber>')
def GET_validate_new_phonenumber(phonenumber):
	c = cleaner.find(phonenumber=phonenumber)
	if c:
		return respond500(str("User with phone number " + phonenumber + " already exists"))
	try:
		twilio_tools.send_SMS(phonenumber, "Welcome to Clean Slate!")
		return respond200()
	except Exception as e:
		return respond500(e)

#POST 		/api/cleaner/<id>/list
@bp.route('/cleaner/<cleaner_id>/list', methods=['POST'])
def POST_list(cleaner_id):
	try:
		list_id = cleaner.add_list(cleaner_id)
		return dumpJSON({ '_id': list_id })
	except Exception as e:
		return respond500(e)

# GET 				/api/list/search
@bp.route('/list/search', methods=['GET'])
def GET_list_search():
	""" 
	Returns List []
	Parameters:
		_cleaner  -> search by cleaner 
	searches all if no parameters
	"""
	try:
		if '_cleaner' in request.args:
			result = List.find(_cleaner=request.args['_cleaner'])
		else:
			result = List.find()
		return dumpJSON(result)
	except Exception as e:
		return respond500(e)

# GET 	/api/list/<id>
@bp.route('/list/<id>', methods=['GET'])
def GET_list_by_id(id):
	try:
		result = List.find(id=id) # returns list 
		return dumpJSON(result[0] if result else None)
	except Exception as e:
		return respond500(e)

# PUT 	/api/list/<id>
@bp.route('/list/<id>', methods=['PUT'])
def PUT_list(id):
	try:
		data = json.loads(request.data)
		List.update(id, data)
		return respond200()
	except Exception as e:
		return respond500(e)

# DELETE 	/api/list/<id>
@bp.route('/list/<id>', methods=['DELETE'])
def DELETE_list(id):
	try:
		List.delete(id)
		return respond200()
	except Exception as e:
		return respond500(e)

# POST 		/api/list/<id>/room
@bp.route('/list/<list_id>/room', methods=['POST'])
def POST_room(list_id):
	try:
		room_id = List.add_room(list_id)
		return dumpJSON({ '_id': room_id })
	except Exception as e:
		return respond500(e)

# GET 		/api/room/search  ?_list=list._id | returns all
@bp.route('/room/search', methods=['GET'])
def GET_room_search():
	""" 
	Returns List []
	Parameters:
		_list  -> search by list
	searches all if no parameters
	"""
	try:
		if '_list' in request.args:
			result = room.find(_list=request.args['_list'])
		else:
			result = room.find()
		return dumpJSON(result)
	except Exception as e:
		return respond500(e)



# POST,PUT 			/api/list/<id>/send

# GET,PUT,DELETE 	/api/room/<id>
# POST,PUT 			/api/room/<id>/task

