
from base import *



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
		rv = self.POST_data('/api/list/' + self.list_id + '/room', data=TEST_ROOM_DATA)
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
		self.assertDataMatch(NEW_CLEANER_DATA, c, keys=['name', 'phonenumber'])
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
		self.PUT_data('/api/list/' + self.list_id, TEST_LIST_DATA)
		data = self.GET_data('/api/list/' + self.list_id)
		self.assertDataMatch(TEST_LIST_DATA, data)
		self.validate_last_modified(data)
		# change data again
		NEW_LIST_DATA = {
			'name': 'NEW-LIST-NAME',
			'phonenumber': '2223334444',
			'location': {
				'address': '4 Salem st',
				'city': 'Cambridge',
				'logitude': '113094234',
				'latitude': '343459',
			},
			'price': '111',
		}
		self.PUT_data('/api/list/' + self.list_id, NEW_LIST_DATA)
		data = self.GET_data('/api/list/' + self.list_id)
		self.assertDataMatch(NEW_LIST_DATA, data)
		self.validate_last_modified(data)
		# didn't change notes -- verify
		self.assertEqual(TEST_LIST_DATA['notes'], data['notes'])


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
		self.POST_list()
		rooms_list_before = self.GET_data('/api/list/' + self.list_id)['rooms']

		# after posting list, cleaner's lists should contain id of posted list
		rv = self.app.post('/api/list/' + self.list_id + '/room')
		room_id = json.loads(rv.data)["_id"]
		rooms_list_after = self.GET_data('/api/list/' + self.list_id)['rooms']
		self.assertEqual(len(rooms_list_before) + 1, len(rooms_list_after))
		self.assertTrue(room_id in rooms_list_after)

	def test_PUT_room(self):
		"""
		1) POST_room
		2) update room data with just count and name 
		3) ensure room still has originally posted data other than count and name 
		4) ensure count and name updated
		"""
		# 1)
		self.POST_room()
		# 2)
		NEW_ROOM_DATA = {'count': '3', 'name': 'NEW-ROOM-NAME'}
		rv = self.PUT_data('/api/room/' + self.room_id, NEW_ROOM_DATA)
		# 3)
		data = self.GET_data('/api/room/' + self.room_id)
		self.assertDataMatch(TEST_ROOM_DATA, data, ['type'])
		# 4)
		self.assertDataMatch(NEW_ROOM_DATA, data, NEW_ROOM_DATA.keys())
		self.validate_last_modified(data)


	def test_GET_room_search(self):

		# test get all rooms
		self.POST_room()
		data_1 = self.GET_data('/api/room/search')
		self.POST_room()
		data_2 = self.GET_data('/api/room/search')
		self.assertEqual(len(data_1) + 1, len(data_2))

		# test get room by _list
		data = self.GET_data('/api/room/search?_list=53c5c5c7de75d60007bf24cd')
		self.assertEqual(0, len(data))
		self.POST_list()
		self.POST_room()
		search_all_data = self.GET_data('/api/room/search')
		specified_list_data = self.GET_data('/api/room/search?_list=' + self.list_id)
		self.assertNotEqual(0, len(specified_list_data))
		self.assertTrue(len(search_all_data) > len(specified_list_data))

		# test populate_tasks
		self.POST_task(TEST_TASK_DATA)
		data = self.GET_data('/api/room/search?populate_tasks=true&_id=' + self.room_id)
		self.assertEqual(type(data[0]['tasks'][0]), dict)



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


	# GET 		/api/task/search 	returns all
	def test_GET_task_search(self):
		""" 
		Returns List [] of all tasks
		"""
		data = self.GET_data('/api/task/search')
		self.assertEqual(0, len(data))
		task_id = self.POST_task(TEST_TASK_DATA)
		data = self.GET_data('/api/task/search')
		self.assertEqual(1, len(data))
		self.assertEqual(task_id, data[0]['_id'])
		self.assertDataMatch(TEST_TASK_DATA, data[0], keys=[k for k in TEST_TASK_DATA.keys()])




