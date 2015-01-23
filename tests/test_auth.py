
from base import *
from app.models import cleaner # need to user cleaner.find to get otherwise unaccessible fields like reset-code and salt
import vcr

class AuthTestCase(BaseTestCase):
	"""
	Test the sign-in flow and logouts
	"""
	@vcr.use_cassette('tests/vcr_cassettes/twilio.yaml')
	def test_reset_password(self):
		""" 2 step process:
				POST,PUT /send-reset-code which sets temporary reset_code in cleaner model and sends via SMS to cleaner
				POST,PUT /reset-password with {'phonenumber', 'reset_code', 'password'}
				--> resets password and logs in cleaner
		"""
		NEW_PASSWORD = 'NEW-PASSWORD'
		# verify process works with correct reset-code
		self.POST_cleaner()
		self.POST_data('/auth/send-reset-code', data=TEST_CLEANER_DATA)
		c = cleaner.find_one(id=self.cleaner['_id'])
		self.POST_data('/auth/reset-password', data={
				'password': 'NEW-PASSWORD',
				'phonenumber': TEST_CLEANER_DATA['phonenumber'],
				'reset_code': c['reset_code'],
				})
		# verify user now logged in
		data = self.GET_data('/auth/user')
		self.assertEqual(data['name'], TEST_CLEANER_DATA['name'])

		# logout user and verify user cannot sign in with old password
		self.logout()
		rv = self.app.post('/auth/login', data=json.dumps({
			'password': TEST_CLEANER_DATA['password'],
			'phonenumber': TEST_CLEANER_DATA['phonenumber']})
		)
		self.assertEqual(rv.status_code, 500)

		# verify user can login with new password
		rv = self.app.post('/auth/login', data=json.dumps({
			'password': NEW_PASSWORD,
			'phonenumber': TEST_CLEANER_DATA['phonenumber']})
		)
		self.assertEqual(rv.status_code, 200)



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

	# GET 	/api/cleaner/validate-new-phonenumber ?phonenumber=cleaner.phonenumber&name=cleaner.name
	@vcr.use_cassette('tests/vcr_cassettes/twilio.yaml')
	def test_validate_new_phonenumber(self):
		endpoint = ('/api/cleaner/validate-new-phonenumber?phonenumber=' + str(TEST_CLEANER_DATA['phonenumber']) + '&name=' + TEST_CLEANER_DATA['name'])
		rv = self.app.get(endpoint)
		self.assertEqual(rv.status_code, 200)
		# POST cleaner - phonenumber will no longer be valid and should generate error
		self.POST_cleaner()
		rv = self.app.get(endpoint)
		self.assertEqual(rv.status_code, 500)

