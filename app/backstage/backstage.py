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
# 	/backstage/backstage.py
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request, send_file

from app.lib.util import dumpJSON, respond500
from app.models import cleaner, list as List, room, task



bp = Blueprint('backstage', __name__, static_folder='static')



@bp.route('/')
def view():
	"""
	TODO: Administration only
	"""
	return send_file('backstage/static/backstage.html')


@bp.route('/data/all', methods=['GET'])
def GET_data_all():
	"""
	Return all the cleaners with all their lists with all their rooms with all their tasks -- HUGE JOIN
	"""
	try:
		all_cleaners = cleaner.find()
		for c in all_cleaners:
			c['lists'] = List.find(_cleaner=c['_id'])
			for l in c['lists']:
				l['rooms'] = room.find(_list=l['_id'], populate_tasks=True)

		return dumpJSON(all_cleaners)

	except Exception as e:
		return respond500(e)













