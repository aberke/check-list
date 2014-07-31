

from base import *




class ViewsTestCase(BaseTestCase):


	# - Utility Methods ----------------------------------------------

	def expect_view_200(self, endpoint):
		""" Helper that gets the page and expects 200 status and content """
		rv = self.app.get(endpoint)
		self.assertEqual(rv.status_code, 200)
		self.assertTrue(int(rv.headers['Content-Length']) > 500)

	def expect_redirect_302(self, endpoint):
		rv = self.app.get(endpoint)
		self.assertEqual(rv.status_code, 302)

	# ----------------------------------------------- Utility Methods -


	def test_base(self):
		self.expect_view_200('/')

	def test_client_views(self):
		self.expect_view_200('/receipt/1')
		self.expect_view_200('/list/1/agreement')

	def test_no_user_views(self):
		""" For following views should redirect to /dashboard if user signed in, 
			otherwise returns base 
				/, /new, /sign-in, /reset-password
		"""
		# before logging in expect 200's
		self.expect_view_200('/')
		self.expect_view_200('/new')
		self.expect_view_200('/sign-in')
		self.expect_view_200('/reset-password')

		# after logging in expect 302
		self.login()
		self.expect_redirect_302('/')
		self.expect_redirect_302('/new')
		self.expect_redirect_302('/sign-in')
		self.expect_redirect_302('/reset-password')


	def test_user_views(self):
		""" Redirect to '/' if no user signed in for following endpoints: 
				/dashboard, /list/<id>
		"""
		self.expect_redirect_302('/dashboard')
		self.expect_redirect_302('/list/2')
		self.expect_redirect_302('/list/2/clean')

		# after logging in should get 200
		self.login()
		self.expect_view_200('/dashboard')
		self.expect_view_200('/list/2/clean')


