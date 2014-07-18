
from base import *



class BackstageTestCase(BaseTestCase):

	def test_views(self):
		# backstage view is protected with basic auth
		rv = self.app.get('/backstage/')
		self.assertEqual(rv.status_code, 401)
		rv = self.GET_basic_auth_protected('/backstage/')
		self.assertEqual(rv.status_code, 200)
		self.assertTrue(int(rv.headers['Content-Length']) > 500)


	def test_data_all(self):
		# initially should get no data
		data = self.GET_data('/backstage/data/all')
		self.assertEqual([], data)

		# post 1 cleaner and expect to get cleaner with empty lists list and expected data
		self.POST_cleaner()
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(1, len(data))
		self.assertEqual([], data[0]['lists'])
		self.assertDataMatch(TEST_CLEANER_DATA, data[0], ['name', 'phonenumber'])

		# post list and expect to get list
		rv = self.POST_data('/api/cleaner/{0}/list'.format(self.cleaner['_id']))
		list_id = json.loads(rv.data)['_id']
		self.PUT_data('/api/list/{0}'.format(list_id), data=TEST_LIST_DATA)
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(1, len(data))
		self.assertEqual(1, len(data[0]['lists']))
		self.assertDataMatch(TEST_LIST_DATA, data[0]['lists'][0], TEST_LIST_DATA.keys())

		# post task and expect to get task data
		rv = self.POST_data('/api/list/{0}/room'.format(list_id), data=TEST_ROOM_DATA)
		room_id = json.loads(rv.data)['_id']
		# post task to last room
		rv = self.POST_data('/api/room/{0}/task'.format(room_id), data=TEST_TASK_DATA)
		# expect to get that task
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(1, len(data))
		self.assertEqual(1, len(data[0]['lists']))
		num_rooms = len(data[0]['lists'][0]['rooms'])
		self.assertTrue(num_rooms > 0)
		last_room = data[0]['lists'][0]['rooms'][num_rooms-1]
		self.assertDataMatch(TEST_ROOM_DATA, last_room, TEST_ROOM_DATA.keys())
		self.assertEqual(1, len(last_room['tasks']))
		self.assertDataMatch(TEST_TASK_DATA, last_room['tasks'][0], TEST_TASK_DATA.keys())

		# post an additional task and make sure can get both
		rv = self.POST_data('/api/room/{0}/task'.format(room_id), data={'name': 'ANOTHER-TASK'})
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(1, len(data))
		self.assertEqual(1, len(data[0]['lists']))
		num_rooms = len(data[0]['lists'][0]['rooms'])
		self.assertTrue(num_rooms > 0)
		last_room = data[0]['lists'][0]['rooms'][num_rooms-1]
		self.assertDataMatch(TEST_ROOM_DATA, last_room, TEST_ROOM_DATA.keys())
		self.assertEqual(2, len(last_room['tasks']))

		# post additional room and make sure now get 1 more room than last GET
		rv = self.POST_data('/api/list/{0}/room'.format(list_id), data=TEST_ROOM_DATA)
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(1, len(data))
		self.assertEqual(1, len(data[0]['lists']))
		self.assertEqual(num_rooms + 1, len(data[0]['lists'][0]['rooms']))

		# post additional list and make sure now get 2 lists
		rv = self.POST_data('/api/cleaner/{0}/list'.format(self.cleaner['_id']))
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(1, len(data))
		self.assertEqual(2, len(data[0]['lists']))

		# post additional cleaner and make sure now get 2 cleaners
		self.POST_data('/api/cleaner', data={'name': 'ADDITIONAL-CLEANER', 'phonenumber': '2223334444', 'password': 'ADDITIONAL-PASSWORD'})
		data = self.GET_data('/backstage/data/all')
		self.assertEqual(2, len(data))
