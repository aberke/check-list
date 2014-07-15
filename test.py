import os
import json
import unittest
import dateutil.parser
from datetime import datetime


# Set ENVIRONMENT=TESTING before loading any packages so that they load with the TESTING configuration
# config.py checks environment variable ENVIRONMENT for setting: MONGODB_DB,
os.environ["ENVIRONMENT"] = "TESTING"

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
	'_cleaner': '',
	'name': 'TEST-LIST',
	'phonenumber': '6178348458',
	'location': 'TEST-LOCATION',
}
TEST_ROOM_DATA = {
	'_list': '',
	'name': 'LIVINGROOM',
	'type': 'livingroom',
}
TEST_TASK_DATA = {
	'name': 'vacuum',
	'room_type': 'bedroom',
	'selected': 'true',
	'default': 'true',
}


class BaseTestCase(unittest.TestCase):

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
		return self.app.post('/auth/login', data=json.dumps(TEST_CLEANER_DATA))

	def logout(self):
		return self.app.get('/auth/logout', follow_redirects=True)

	def validate_last_modified(self, data):
		""" Asserts that data has a 'last_modified' field and that date is before now """
		self.assertTrue('last_modified' in data)
		now = datetime.now()
		self.assertTrue(dateutil.parser.parse(data['last_modified']) > now)

	# ----------------------------------------------- Utility Methods -

	def test_views(self):
		rv = self.app.get('/')
		self.assertEqual(rv.status_code, 200)
		self.assertTrue(int(rv.headers['Content-Length']) > 500)


class APITestCase(BaseTestCase):
	"""
	POST_cleaner implicitely tested
	"""
	cleaner = None 
	list_id = None
	room_id = None

	def setUp(self):
		super(APITestCase, self).setUp()
		self.POST_cleaner()
		self.logout()

	def POST_list(self):
		""" Helper method to post the list and keep returned list id as self.list_id """
		rv = self.app.post('/api/cleaner/{0}/list'.format(self.cleaner['_id']))
		self.assertEqual(rv.status_code, 200)
		self.list_id = json.loads(rv.data)['_id']

	def POST_room(self):
		""" Helper method to post list, then room and keep returned room id as self.room_id """
		if not self.list_id:
			self.POST_list()
		rv = self.POST_data('/api/list/' + self.list_id + '/room')
		self.assertEqual(rv.status_code, 200)
		self.room_id = json.loads(rv.data)['_id']

	def POST_task(self, task_data):
		""" Helper method to tests.
			Posts task data to room with self.room_id
			Returns id of newly inserted task
		"""
		if not self.room_id:
			self.POST_room()
		rv = self.POST_data('/api/room/' + self.room_id + '/task', data=task_data)
		self.assertEqual(rv.status_code, 200)
		return json.loads(rv.data)['_id']		


	def test_PUT_cleaner(self):
		NEW_CLEANER_DATA = {
			'name': 'NEW-NAME',
			'phonenumber': '2223334444',
		}
		self.PUT_data('/api/cleaner/' + self.cleaner['_id'], NEW_CLEANER_DATA)
		c = self.GET_data('/api/cleaner/' + self.cleaner['_id'])
		self.assertDataMatch(NEW_CLEANER_DATA, c, ['name', 'phonenumber'])
		self.validate_last_modified(c)


	def test_GET_cleaner_search(self):
		# test GET all
		data = self.GET_data('/api/cleaner/search')
		self.assertEqual(type([]), type(data))
		self.assertEqual(1, len(data))
		self.assertEqual(self.cleaner['_id'], data[0]['_id'])

		# test GET by phonenumber
		data = self.GET_data('/api/cleaner/search?phonenumber=' + 'BAD-PHONENUMBER')
		self.assertEqual([], data)
		data = self.GET_data('/api/cleaner/search?phonenumber=' + self.cleaner['phonenumber'])
		self.assertEqual(1, len(data))
		self.assertEqual(self.cleaner['_id'], data[0]['_id'])


	def test_GET_cleaner_by_id(self):
		c = self.GET_data('/api/cleaner/' + self.cleaner['_id'])
		self.assertDataMatch(self.cleaner, c, keys=['phonenumber', 'name', '_id'])
		c = self.GET_data('/api/cleaner/' + '53bed5c2b81c823ab1ee66a4')
		self.assertEqual(None, c)


	def test_POST_list(self):
		""" POST_list main functionality implicitely tested by other tests 
				verify list added to cleaner's lists 
		"""
		# cleaner's lists should originally be empty
		data = self.GET_data('/api/cleaner/' + self.cleaner['_id'])
		self.assertEqual([], data['lists'])

		# after posting list, cleaner's lists should contain just id of posted list
		self.POST_list()
		data = self.GET_data('/api/cleaner/' + self.cleaner['_id'])
		self.assertEqual(1, len(data['lists']))
		self.assertEqual(self.list_id, data['lists'][0])


	def test_GET_list_search(self):
		# test get all lists
		data = self.GET_data('/api/list/search')
		self.assertEqual([], data)
		self.POST_list()
		data = self.GET_data('/api/list/search')
		self.assertEqual(1, len(data))
		self.assertEqual(self.list_id, data[0]['_id'])

		# test get list by _cleaner
		data = self.GET_data('/api/list/search?_cleaner=' + self.cleaner['_id'])
		self.assertEqual(1, len(data))
		self.assertEqual(self.list_id, data[0]['_id'])
		self.POST_list()
		data = self.GET_data('/api/list/search?_cleaner=' + self.cleaner['_id'])
		self.assertEqual(2, len(data))


	def test_GET_list_by_id(self):
		data = self.GET_data('/api/list/53beef98b81c823c51e64a7b')
		self.assertEqual(data, None)
		self.POST_list()
		data = self.GET_data('/api/list/' + self.list_id)
		self.assertEqual(self.list_id, data['_id'])


	def test_PUT_list(self):
		self.POST_list()
		NEW_LIST_DATA = {
			'name': 'NEW-LIST-NAME',
			'phonenumber': '2223334444',
			'location': {
				'address': '4 Salem st',
				'city': 'Cambridge',
				'logitude': '113094234',
				'latitude': '343459',
			}
		}
		self.PUT_data('/api/list/' + self.list_id, NEW_LIST_DATA)
		data = self.GET_data('/api/list/' + self.list_id)
		self.assertDataMatch(NEW_LIST_DATA, data)
		self.validate_last_modified(data)


	def test_DELETE_list(self):
		# post a list and room, then delete list; cleaner already posted in setUp and POST_room implicitely posts list as well
		self.POST_room()
		self.DELETE('/api/list/' + self.list_id)

		# verify doesn't show up in search and search by id
		data = self.GET_data('/api/list/' + self.list_id)
		self.assertEqual(None, data)
		data = self.GET_data('/api/list/search')
		self.assertEqual([], data)

		# verify list's cleaner no longer references list
		c = self.GET_data('/api/cleaner/' + self.cleaner['_id'])
		self.assertEqual([], c['lists'])


	def test_POST_room(self):
		""" POST_room main functionality implicitely tested by other tests 
				verify list added to list's rooms
		"""
		# TODO - FIX THIS
		# COMMENTED OUT WHILE DOING DEFAULT ROOMS WHEN POST LIST

		# list's rooms should originally be empty
		# self.POST_list()
		# data = self.GET_data('/api/list/' + self.list_id)
		# self.assertEqual([], data['rooms'])

		# # after posting list, cleaner's lists should contain just id of posted list
		# rv = self.app.post('/api/list/' + self.list_id + '/room')
		# room_id = json.loads(rv.data)["_id"]
		# data = self.GET_data('/api/list/' + self.list_id)
		# self.assertEqual(1, len(data['rooms']))
		# self.assertEqual(room_id, data['rooms'][0])
		pass


	def test_GET_room_search(self):
		# TODO - FIX THIS
		# COMMENTED OUT WHILE DOING DEFAULT ROOMS WHEN POST LIST

		# test get all rooms
		# data = self.GET_data('/api/room/search')
		# self.assertEqual([], data)
		# self.POST_room()
		# data = self.GET_data('/api/room/search')
		# self.assertEqual(1, len(data))
		# self.assertEqual(self.room_id, data[0]['_id'])

		# # test get room by _list
		# data = self.GET_data('/api/room/search?_list=' + self.list_id)
		# self.assertNotEqual(1, len(data))
		# self.assertEqual(self.room_id, data[0]['_id'])
		# self.POST_room()
		# data = self.GET_data('/api/room/search?_list=' + self.list_id)
		# self.assertEqual(2, len(data))
		pass


	#GET 	/api/room/<id>
	def test_GET_room_by_id(self):
		""" POST 3 rooms and verify get just the one specified """
		data = self.GET_data('/api/room/53c47cdbb81c825566b1a9e2')
		self.assertEqual(data, None)
		self.POST_room()
		self.POST_room()
		specified_room_id = self.POST_room()
		data = self.GET_data('/api/room/' + self.room_id)
		self.assertNotEqual(data, None)
		self.assertEqual(data["_id"], self.room_id)


	# POST 	 	/api/room/<id>/task
	def test_POST_task(self):
		self.POST_room()
		# room should initially have no tasks
		self.POST_room()
		data = self.GET_data('/api/room/' + self.room_id)
		self.assertEqual(data["tasks"], [])
		# after posting a task, room should have reference to task
		task_id = self.POST_task(TEST_TASK_DATA)
		data = self.GET_data('/api/room/' + self.room_id)
		self.assertEqual(1, len(data["tasks"]))
		self.assertEqual(task_id, data["tasks"][0])

	# DELETE 	/api/task/<id>
	def test_DELETE_task(self):
		""" Posts 3 tasks and then deletes 2 """
		task_id_1 = self.POST_task(TEST_TASK_DATA)
		task_id_2 = self.POST_task(TEST_TASK_DATA)
		task_id_3 = self.POST_task(TEST_TASK_DATA)
		data = self.GET_data('/api/room/' + self.room_id)
		self.assertEqual(3, len(data["tasks"]))
		# delete tasks 1 and 3 and verify just have task 2
		self.DELETE('/api/task/' + task_id_1)
		self.DELETE('/api/task/' + task_id_3)
		data = self.GET_data('/api/room/' + self.room_id)
		self.assertEqual(1, len(data["tasks"]))
		self.assertEqual(task_id_2, data["tasks"][0])


	
	# TODO
	# GET 		/api/room/search  ?[populate_tasks=boolean]&[_list=list._id | returns all]

	# GET 		/api/task/search 	returns all






class AuthTestCase(BaseTestCase):
	"""
	Test the sign-in flow and logouts 
	"""

	def test_login_logout(self):
		# get user should return null
		data = self.GET_data('/auth/user')
		self.assertEqual(data, None)

		# can't login with no users in database
		rv = self.login()
		self.assertEqual(rv.status_code, 500)

		#posting new cleaner should automatically log that cleaner in
		rv = self.POST_cleaner()
		self.assertEqual(rv.status_code, 200)
		data = self.GET_data('/auth/user')
		self.assertEqual(data['name'], TEST_CLEANER_DATA['name'])

		#test logout
		rv = self.logout()
		self.assertEqual(rv.status_code, 200)
		data = self.GET_data('/auth/user')
		self.assertEqual(data, None)

		#logging in with invalid phonenumber should fail
		rv = self.app.post('/auth/login', data=json.dumps({
			'password': TEST_CLEANER_DATA['password'],
			'phonenumber': 'INVALID-PHONENUMBER'})
		)
		self.assertEqual(rv.status_code, 500)

		#logging in with invalid password should fail
		rv = self.app.post('/auth/login', data=json.dumps({
			'password': 'INVALID-PASSWORD',
			'phonenumber': TEST_CLEANER_DATA['phonenumber']})
		)
		self.assertEqual(rv.status_code, 500)

		#logging in with valid credentials should work
		rv = self.login()
		self.assertEqual(rv.status_code, 200)
		data = self.GET_data('/auth/user')
		self.assertEqual(data['name'], TEST_CLEANER_DATA['name'])

	def test_validate_new_phonenumber(self):
		rv = self.app.get('/api/cleaner/validate-new-phonenumber/' + TEST_CLEANER_DATA['phonenumber'])
		self.assertEqual(rv.status_code, 200)
		# POST cleaner - phonenumber will no longer be valid and should generate error
		self.POST_cleaner()
		rv = self.app.get('/api/cleaner/validate-new-phonenumber/' + TEST_CLEANER_DATA['phonenumber'])
		self.assertEqual(rv.status_code, 500)



class ModelTestCase(BaseTestCase):

	def setUp(self):
		super(ModelTestCase, self).setUp()
		self.insert_cleaner()

	def insert_cleaner(self):
		""" Helper to insert cleaner into database """
		id = cleaner.insert_new(TEST_CLEANER_DATA)
		self.cleaner_id = id
		return id



class CleanerModelTestCase(ModelTestCase):
	"""
	insert_new implicitely tested by other test cases
	"""

	def test_find_one(self):
		""" find_one uses find so find implicitely tested? """
		TEST_CLEANER_DATA['_id'] = self.cleaner_id
		test_keys = ['_id', 'name', 'phonenumber']
		# find all
		c = cleaner.find_one(id=self.cleaner_id)
		self.assertDataMatch(TEST_CLEANER_DATA, c, keys=test_keys)
		# test get cleaner by id
		c = cleaner.find_one(id=self.cleaner_id)
		self.assertDataMatch(TEST_CLEANER_DATA, c, keys=test_keys)
		# test get cleaner by phonenumber
		c = cleaner.find_one(phonenumber=TEST_CLEANER_DATA['phonenumber'])
		self.assertDataMatch(TEST_CLEANER_DATA, c, keys=test_keys)

	def test_update(self):
		new_data = {
			'hashed_pwd': '1',
			'a': '2',
			'b': '3',
		}
		cleaner.update(self.cleaner_id, new_data)
		c = cleaner.find_one(id=self.cleaner_id)
		self.assertDataMatch(new_data, c)

	def test_public(self):
		c = cleaner.find_one(id=self.cleaner_id)
		profile = cleaner.public(c)
		self.assertNotIn('password', profile)
		self.assertNotIn('hashed_pwd', profile)
		self.assertNotIn('salt', profile)

	def test_find_public(self):
		profile = cleaner.find_public(id=self.cleaner_id)
		self.assertNotIn('password', profile)
		self.assertNotIn('hashed_pwd', profile)
		self.assertNotIn('salt', profile)








if __name__ == '__main__':
    unittest.main()