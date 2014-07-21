import json
import unittest
import dateutil.parser
from datetime import datetime
from base64 import b64encode # for basic auth

import config
from app import app
from app import database
from app.models import cleaner



# the test data that will be injected
TEST_CLEANER_DATA = {
	'name': 'TEST-NAME',
	'phonenumber': '6178883333',
	'password': 'TEST-PASSWORD',
}
TEST_LIST_DATA = {
	'name': 'TEST-LIST',
	'phonenumber': '6178348458',
	'location': 'TEST-LOCATION',
	'notes': 'TEST-NOTES TEST-NOTES TEST-NOTES TEST-NOTES TEST-NOTES TEST-NOTES ',
	'price': '123',
}
TEST_ROOM_DATA = {
	'name': 'LIVINGROOM',
	'type': 'living-room',
}
TEST_TASK_DATA = {
	'name': 'vacuum',
	'room_type': 'bedroom',
	'selected': 'true',
	'default': 'true',
}


class BaseTestCase(unittest.TestCase):

	cleaner = None

	# - Setup/Teardown -----------------------------------------------
	def setUp(self):
		app.config['TESTING'] = True
		self.app = app.test_client()

	def tearDown(self):
		database.drop_all()
		self.logout()
	# ----------------------------------------------- Setup/Teardown -

	# - Utility Methods ----------------------------------------------
	def assertDataMatch(self, test_data, response_data, keys=None):
		""" Assert test_data and response_data match across keys or test_data.keys()"""
		keys = keys if keys else test_data.keys()
		for test_key in keys:
			self.assertEqual(test_data[test_key], response_data[test_key])

	def GET_basic_auth_protected(self, endpoint):
		""" requires_auth decorator in lib/basic_auth verifies that request made with BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD
			or sends 401
		"""
		BASIC_AUTH_USERNAME = config.BASIC_AUTH_USERNAME
		BASIC_AUTH_PASSWORD = config.BASIC_AUTH_PASSWORD
		headers = {
    		'Authorization': 'Basic ' + b64encode("{0}:{1}".format(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))
		}
		return self.app.get(endpoint, headers=headers)

	def GET_data(self, endpoint):
		rv = self.app.get(endpoint)
		self.assertEqual(rv.status_code, 200)
		return json.loads(rv.data)

	def POST_data(self, endpoint, data=None):
		data = data if data else {}
		rv = self.app.post(endpoint, data=json.dumps(data))
		self.assertEqual(rv.status_code, 200)
		return rv

	def PUT_data(self, endpoint, data=None):
		data = data if data else {}
		rv = self.app.put(endpoint, data=json.dumps(data))
		self.assertEqual(rv.status_code, 200)
		return rv

	def DELETE(self, endpoint):
		rv = self.app.delete(endpoint)
		self.assertEqual(rv.status_code, 200)
		return rv

	def POST_cleaner(self):
		""" Helper method to post the cleaner and keep returned cleaner as self.cleaner """
		rv = self.POST_data('/api/cleaner', TEST_CLEANER_DATA)
		self.cleaner = json.loads(rv.data)
		return rv

	def login(self):
		if not self.cleaner:
			self.POST_cleaner()
		return self.app.post('/auth/login', data=json.dumps(TEST_CLEANER_DATA))

	def logout(self):
		return self.app.post('/auth/logout', follow_redirects=True)

	def validate_last_modified(self, data):
		""" Asserts that data has a 'last_modified' field and that date is before now """
		self.assertTrue('last_modified' in data)
		now = datetime.now()
		self.assertTrue(dateutil.parser.parse(data['last_modified']) > now)

	# ----------------------------------------------- Utility Methods -