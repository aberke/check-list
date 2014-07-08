import os
import json
import unittest
from datetime import datetime

# Set ENVIRONMENT=TESTING before loading any packages so that they load with the TESTING configuration
# config.py checks environment variable ENVIRONMENT for setting: MONGODB_DB,
os.environ["ENVIRONMENT"] = "TESTING"

from app import app
from app import database
from app.cleaner import auth
from app.cleaner import model



# the test data that will be injected
TEST_CLEANER_DATA = {
	'name': 'TEST-NAME',
	'phonenumber': '6178883333',
	'password': 'TEST-PASSWORD',
}



class BaseTestCase(unittest.TestCase):

	# - Setup/Teardown -----------------------------------------------
	def setUp(self):
		app.config['TESTING'] = True
		self.app = app.test_client()

	def tearDown(self):
		database.drop_all()
	# ----------------------------------------------- Setup/Teardown -

	# - Utility Methods ----------------------------------------------
	def assertDataMatch(self, test_data, response_data, keys=None):
		""" Assert test_data and response_data match across keys or test_data.keys()"""
		keys = keys if keys else test_data.keys()
		for test_key in keys:
			self.assertEqual(test_data[test_key], response_data[test_key])

	def login(self):
		self.app.post('/auth/login', data=json.dumps(test_user_data))
		self.user = self.GETdata('/auth/user')

	def logout(self):
		self.app.get('/auth/logout', follow_redirects=True)
		self.user = None

	def GETdata(self, endpoint):
		rv = self.app.get(endpoint)
		self.assertEqual(rv.status_code, 200)
		return json.loads(rv.data)
	# ----------------------------------------------- Utility Methods -

	def test_views(self):
		rv = self.app.get('/')
		self.assertEqual(rv.status_code, 200)
		self.assertTrue(int(rv.headers['Content-Length']) > 500)


class AuthTestCase(BaseTestCase):
	"""
	Test the sign-in flow and logouts 
	"""

	def test_TODO(self):
		print('WRITE THESE TESTS')



class ModelTestCase(BaseTestCase):
	"""
	insert_new_cleaner implicitely tested by other test cases
	"""

	def insert_cleaner(self):
		""" Helper to insert cleaner into database """
		return model.insert_new_cleaner(TEST_CLEANER_DATA)

	def test_get_all(self):
		all = model.get_all()
		self.assertEqual([], [c for c in all])

	def test_get_cleaner(self):
		id = self.insert_cleaner()
		TEST_CLEANER_DATA['_id'] = id
		test_keys = ['_id', 'name', 'phonenumber']
		# test get cleaner by id
		cleaner = model.get_cleaner(id=id)
		self.assertDataMatch(TEST_CLEANER_DATA, cleaner, keys=test_keys)
		# test get cleaner by phonenumber
		cleaner = model.get_cleaner(phonenumber=TEST_CLEANER_DATA['phonenumber'])
		self.assertDataMatch(TEST_CLEANER_DATA, cleaner, keys=test_keys)

	def test_update_cleaner(self):
		id = self.insert_cleaner()
		new_data = {
			'hashed_pwd': '1',
			'a': '2',
			'b': '3',
		}
		model.update_cleaner(id, new_data)
		cleaner = model.get_cleaner(id=id)
		self.assertDataMatch(new_data, cleaner)

	def test_public_profile(self):
		id = self.insert_cleaner()
		cleaner = model.get_cleaner(id=id)
		profile = model.public_cleaner(cleaner)
		self.assertNotIn('password', profile)
		self.assertNotIn('hashed_pwd', profile)
		self.assertNotIn('salt', profile)



class CleanerTestCase(BaseTestCase):


	def test_cleaner_all(self):
		""" test call to /cleaner/all """
		data = self.GETdata('/cleaner/all')
		self.assertEqual([], data)







if __name__ == '__main__':
    unittest.main()