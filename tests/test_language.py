
from base import *
import config


SUPPORTED_LANGUAGES = config.SUPPORTED_LANGUAGES


class LanguageTestCase(BaseTestCase):
	"""
	Tests for the language module
	module has a blueprint with endpoints that interface with the client side translate service
	tests insure that
		static assets are accessible: (client side angularJS module)
		server side endpoints and module work
	"""

	def test_static_assets(self):
		self.expect_view_200('/language/static/translateModule/filters.js')
		self.expect_view_200('/language/static/translateModule/services.js')
		self.expect_view_200('/language/static/translateModule/module.js')


	def test_GET_map(self):
	    """
	    Returns the formatted language map.
	    Data pulled from google spreadsheet and then formatted as
	    {
	      keyname: {
	          en: "english translation",
	          es: "spanish translation",
	          ... for column/language in spreadsheet
	      },
	      ... for row/keyname in spreadsheet
	    """
	    map = self.GET_data('/language/map')
	    self.assertTrue(len(map.keys()) > 20)
	    for key in map.keys():
	    	for lang in SUPPORTED_LANGUAGES:
	    		self.assertTrue(lang in map[key])


	def test_language_setting(self):
		"""
		These are the endpoints that the angularJS service interfaces with for handling current language
		language-setting is stored in session

		POST 	/language/setting
		GET  	/language/setting
		DELETE  /language/setting/clear
		"""
		# when first GET language-setting, should be null
		data = self.GET_data('/language/setting')
		self.assertEqual(None, data['language-setting'])

		# setting language setting to invalid value should return error
		rv = self.app.post('/language/setting', data=json.dumps({'language-setting': 'INVALID-LANGUAGE'}))
		self.assertEqual(rv.status_code, 500)

		# setting language-setting to supported language should work
		for lang in SUPPORTED_LANGUAGES:
			self.POST_data('/language/setting', data={ 'language-setting': lang })
			data = self.GET_data('/language/setting')
			self.assertEqual(lang, data['language-setting'])

		# DELETE /language/setting should clear language-setting back to null
		self.DELETE('/language/setting')
		data = self.GET_data('/language/setting')
		self.assertEqual(None, data['language-setting'])



















