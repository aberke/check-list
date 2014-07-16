
from base import *


class ModelTestCase(BaseTestCase):

	cleaner_id = None

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
		test_keys = ['name', 'phonenumber']
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
			'name': '2',
			'phonenumber': '3',
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




