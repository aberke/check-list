
from base import *


class AuthTestCase(BaseTestCase):
	"""
	Test the sign-in flow and logouts 
	"""

	def test_login_logout(self):
		# get user should return null
		data = self.GET_data('/auth/user')
		self.assertEqual(data, None)

		# can't login with no users in database
		rv = self.app.post('/auth/login', data=json.dumps(TEST_CLEANER_DATA)
		)
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

