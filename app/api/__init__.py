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
# 	/api/__init__.py
#
# 	API endpoints
# 	-------------------------
# GET 				/api/cleaner/validate-new-phonenumber ?phonenumber=cleaner.phonenumber&name=cleaner.name
# POST 				/api/cleaner
# GET 				/api/cleaner/search ?phonenumber=phonenumber || returns all
# GET,PUT 			/api/cleaner/<id>
# POST 				/api/cleaner/<id>/list
#
# GET 				/api/list/search ?[_id=list._id]&[populate_rooms=boolean]&[_cleaner=cleaner._id | returns all]
# GET,PUT,DELETE 	/api/list/<id>   ?[populate_cleaner=boolean] TODO: TEST coverage for populate_cleaner
# POST,PUT 			/api/list/<list_id>/send -- sends AGREEMENT
# POST 				/api/list/<id>/room
#
# GET 				/api/room/search ?[populate_tasks=boolean]&[_list=list._id | returns all]
# GET,PUT,DELETE 	/api/room/<id>
# POST 	 			/api/room/<id>/task

# GET 				/api/task/search returns all
# DELETE 			/api/task/<id>

# POST 				/api/list/<id>/receipt -- sends RECEIPT
# GET 				/api/receipt/<id>

#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request, session, redirect
import json

import config
from app.lib.util import yellERROR, dumpJSON, respond500, respond200
from app.lib import twilio_tools
from app.lib.util import JSONencoder
from app import auth
from app.models import cleaner, list as List, room, task, receipt



bp = Blueprint('api', __name__)



#POST 		/api/cleaner
@bp.route('/cleaner', methods=['POST'])
def POST_cleaner():
	""" Insert and login new cleaner """
	try:
		data = JSONencoder.load(request.data)
		id = cleaner.insert_new(data)
		c = cleaner.find_public(id=id)
		auth.login(c)
		return dumpJSON(c)
	except Exception as e:
		return respond500(err=e, code=0)

# PUT 	/api/cleaner/<id>
@bp.route('/cleaner/<id>', methods=['PUT'])
def PUT_cleaner(id):
	try:
		data = JSONencoder.load(request.data)
		cleaner.update(id, data)
		return respond200()
	except Exception as e:
		return respond500(err=e, code=0)


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
		return respond500(err=e, code=0)

#GET 	/api/cleaner/<id>
@bp.route('/cleaner/<id>', methods=['GET'])
def GET_cleaner_by_id(id):
	try:
		return dumpJSON(cleaner.find_one(id=id))
	except Exception as e:
		return respond500(err=e, code=0)

# GET 		/api/cleaner/validate-new-phonenumber ?phonenumber=cleaner.phonenumber&name=cleaner.name
@bp.route('/cleaner/validate-new-phonenumber')
def GET_validate_new_phonenumber():
	"""
	Expects phonenumber and name in request arguments
	Validates that phonenumber is new and sends welcome message via SMS
	"""
	try:
		# get name from request
		if 'name' not in request.args:
			return respond500(code=6)
		name = request.args['name']

		# get phonenumber from request
		if 'phonenumber' not in request.args:
			return respond500(code=1)
		phonenumber = request.args['phonenumber']

		# insure phonenumber is new
		if cleaner.find(phonenumber=phonenumber):
			return respond500(code=5)

		twilio_tools.send_welcome(phonenumber, name)
		return respond200()
	except Exception as e:
		return respond500(err=e, code=0)

#POST 		/api/cleaner/<id>/list
@bp.route('/cleaner/<cleaner_id>/list', methods=['POST'])
def POST_list(cleaner_id):
	try:
		list_data = JSONencoder.load(request.data)
		list_id = cleaner.add_list(cleaner_id, list_data=list_data)
		return dumpJSON({ '_id': list_id })
	except Exception as e:
		return respond500(err=e, code=0)


# GET 		/api/list/search ?[populate_rooms=boolean]&[_cleaner=cleaner._id | returns all]
@bp.route('/list/search', methods=['GET'])
def GET_list_search():
	""" 
	Returns List []
	Parameters:
		_id 			-> search by id 
		_cleaner  		-> search by cleaner
		populate_rooms  -> populate rooms list which will also populate tasks list 
	searches all if no parameters
	"""
	try:
		_id 			= request.args['_id'] if '_id' in request.args else None 
		_cleaner 		= request.args['_cleaner'] if '_cleaner' in request.args else None 
		populate_rooms	= request.args['populate_rooms'] if 'populate_rooms' in request.args else None 
		
		result = List.find(id=_id, _cleaner=_cleaner, populate_rooms=populate_rooms)
		return dumpJSON(result)
	except Exception as e:
		return respond500(err=e, code=0)

# GET 	/api/list/<id>	   ?[populate_cleaner=boolean]
@bp.route('/list/<id>', methods=['GET'])
def GET_list_by_id(id):
	try:
		populate_cleaner = request.args['populate_cleaner'] if 'populate_cleaner' in request.args else False 
		result = List.find_one(id=id, populate_cleaner=populate_cleaner) # returns list 
		return dumpJSON(result)
	except Exception as e:
		return respond500(err=e, code=0)

# PUT 	/api/list/<id>
@bp.route('/list/<id>', methods=['PUT'])
def PUT_list(id):
	try:
		data = JSONencoder.load(request.data)
		List.update(id, data)
		return dumpJSON({ '_id': id })
	except Exception as e:
		return respond500(err=e, code=0)


# DELETE 	/api/list/<id>
@bp.route('/list/<id>', methods=['DELETE'])
def DELETE_list(id):
	try:
		List.delete(id)
		return respond200()
	except Exception as e:
		return respond500(err=e, code=0)


# POST,PUT 	/api/list/<id>/send
@bp.route('/list/<id>/send', methods=['PUT', 'POST'])
def PUT_send_list(id):
	"""
	Sends new agreement to client via SMS

	@param 		{id} _id of list to send as agreement to client 
	payload:	Request is made with entire list object - have _cleaner as cleaner._id

	Returns 200 response
	"""
	try:
		list_data = JSONencoder.load(request.data)

		# verify phonenumber in list_data -- need it to send link to receipt to client
		if not 'phonenumber' in list_data:
			return respond500(code=1)
		phonenumber = list_data['phonenumber']

		# need to fetch cleaner for just cleaner's name in SMS message
		cleaner_id = list_data['_cleaner'] # something went wrong with request if _cleaner not in payload
		c = cleaner.find_one(id=cleaner_id)

		# send SMS to client that has link to viewable agreement
		twilio_tools.send_agreement(phonenumber, c['name'], id)
		
		return respond200()
	except Exception as e:
		return respond500(err=e, code=0)


# POST 		/api/list/<id>/receipt
@bp.route('/list/<list_id>/receipt', methods=['POST'])
def POST_receipt(list_id):
	"""
	Creates receipt + sends receipt to client via SMS

	A receipt is a snapshot of the list at time of POST
	When a receipt is posted, the list/receipt models do the work
	list.create_receipt retrieves a fully populated list and inserts the receipt

	@param 		{list_id} _id of list of which to take snapshot and save as receipt 
	payload:	Request is made with entire list object - have _cleaner as cleaner._id

	Returns _id of newly inserted receipt 
	"""
	try:
		list_data = JSONencoder.load(request.data)

		# verify phonenumber in list_data -- need it to send link to receipt to client
		if not 'phonenumber' in list_data:
			return respond500(code=1)
		phonenumber = list_data['phonenumber']

		# need to fetch cleaner for just cleaner's name in SMS message
		cleaner_id = list_data['_cleaner'] # something went wrong with request if _cleaner not in payload
		c = cleaner.find_one(id=cleaner_id)

		# create the receipt that will live forever
		receipt_id = List.create_receipt(list_id)

		# send SMS to client that has link to viewable receipt
		twilio_tools.send_receipt(phonenumber, c['name'], receipt_id)
		
		return dumpJSON({'_id': receipt_id})
	except Exception as e:
		return respond500(err=e, code=0)


# GET 		/api/receipt/<id>
@bp.route('/receipt/<id>', methods=['GET'])
def GET_receipt_by_id(id):
	try:
		return dumpJSON(receipt.find_one(id=id))
	except Exception as e:
		return respond500(err=e, code=0)


# POST 		/api/list/<id>/room
@bp.route('/list/<list_id>/room', methods=['POST'])
def POST_room(list_id):
	try:
		data = JSONencoder.load(request.data)
		room_id = List.add_room(list_id, room_data=data)
		return dumpJSON({ '_id': room_id })
	except Exception as e:
		return respond500(err=e, code=0)

# PUT 		/api/room/<id>
@bp.route('/room/<id>', methods=['PUT'])
def PUT_room(id):
	try:
		data = JSONencoder.load(request.data)
		room.update(id, data=data)
		return dumpJSON({ '_id': id })
	except Exception as e:
		return respond500(err=e, code=0)

#GET 	/api/room/<id>
@bp.route('/room/<id>', methods=['GET'])
def GET_room_by_id(id):
	try:
		return dumpJSON(room.find_one(id=id))
	except Exception as e:
		return respond500(err=e, code=0)


# GET 		/api/room/search  ?[populate_tasks=boolean]&[_list=list._id | returns all]
@bp.route('/room/search', methods=['GET'])
def GET_room_search():
	""" 
	Returns List []
	Parameters:
		_id 			-> limit search to _id (helpful for testing)
		_list  			-> search by list
		populate_tasks  -> populate tasks list
	searches all if no parameters
	"""
	try:
		_id 			= request.args['_id'] if '_id' in request.args else None 
		_list 			= request.args['_list'] if '_list' in request.args else None 
		populate_tasks	= request.args['populate_tasks'] if 'populate_tasks' in request.args else None 

		result = room.find(id=_id, _list=_list, populate_tasks=populate_tasks)
		return dumpJSON(result)
	except Exception as e:
		return respond500(err=e, code=0)

# POST 		/api/room/<id>/task
@bp.route('/room/<room_id>/task', methods=['POST'])
def POST_task(room_id):
	try:
		data = JSONencoder.load(request.data)
		id = room.add_task(room_id, data)
		return dumpJSON({ '_id': id })
	except Exception as e:
		return respond500(err=e, code=0)


# GET 		/api/task/search returns all
@bp.route('/task/search', methods=['GET'])
def GET_task_search():
	""" 
	Returns List [] of all tasks
	"""
	try:
		result = task.find()
		return dumpJSON(result)
	except Exception as e:
		return respond500(err=e, code=0)


# DELETE 	/api/task/<id>
@bp.route('/task/<id>', methods=['DELETE'])
def DELETE_task(id):
	try:
		task.delete(id)
		return respond200()
	except Exception as e:
		return respond500(err=e, code=0)






# GET,DELETE 	/api/room/<id>

