/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014


 	AngularJS translateModule: service

    All Javascript is executed in order it appears on page, so here's order:
        TranslateService defined
        translateMapCallback defined (sets TranslateService.prototype.map)
        languageSettingCallback defined
        CheckList app (Main AngularJS app - app.js) instantiates TranslateService (must happen after callbacks!)

****************************************************/



var TranslateService = function($http) {

	/*
	- Manager of current language {String} languageSetting
	- Called by TranslateFilter to do the work of translation
	- Keeps translations in translateMap:
	{
		keyname: {
			en: "english translation",
			es: "spanish translation",
			... for column/language in spreadsheet
		},
		... for row/keyname in spreadsheet
	}
	translateMap is constructed server-side
	Called in base.html? /translate/map?callback=translateMapCallback (at bottom)
	It's added to prototype on callback of it loading
	Keep it as script (rather than loading from module) so that can ensure loaded in before page renders
	*/


	this.translateMap;
	this.languageSetting;
	var browserLanguageMap = {
		    'en': 'en',
		    'en-gb': 'en',
		    'en-us': 'en',
		    'en-au': 'en',
		    'en-ca': 'en',
		    'en-nz': 'en',
		    'en-ie': 'en',
		    'en-za': 'en',
		    'en-jm': 'en',
		    'en-bz': 'en',
		    'en-tt': 'en',

		    'es': 	 'es',
			'es-do': 'es',
			'es-ar': 'es',
			'es-co': 'es',
			'es-mx': 'es',
			'es-es': 'es',
			'es-gt': 'es',
			'es-cr': 'es',
			'es-pa': 'es',
			'es-ve': 'es',
			'es-pe': 'es',
			'es-ec': 'es',
			'es-cl': 'es',
			'es-uy': 'es',
			'es-py': 'es',
			'es-bo': 'es',
			'es-sv': 'es',
			'es-hn': 'es',
			'es-ni': 'es',
			'es-pr': 'es',
	}
	var detectLanguage = function() {
		/* 	Check the browser for which language is set
			
			Returns {String | null}
				if detected: language 'en' or 'es' 
				else: null
		*/
		// navigator.language for non EI, navigator.userLanguage for IE
		var browserLanguage = (navigator.language || navigator.userLanguage);
		if (!browserLanguage) { return null; } // language not detected

		browserLanguage = browserLanguage.toLowerCase();
		return browserLanguageMap[browserLanguage];
	}

	this.getLanguage = function() {
		return this.languageSetting;
	}
	this.setLanguage = function(language) {
		this.languageSetting = language;

		// remember language choice in server session
		$http.post('/language/setting', {'language-setting': language})
			.error(function(errData) {
				console.log('ERROR in POST /language/setting: ', errData);
			});
	}

	this.translate = function(keyname) {
		/*
		@param {String} keyname -- keyname to look up in translate map and translate
		Returns translation found in translateMap or (untranslated) original keyname if no translation found
		*/
		if (keyname in this.translateMap) {
			return this.translateMap[keyname][this.languageSetting];
		}
		return keyname;
	}

	this.init = function() {
		/* if languageSetting isn't set (server returned null)
			 initialize languageSetting to whichever language user's browser uses. 
			 defaults to english 
		*/
		if (!this.languageSetting) {
			this.setLanguage((detectLanguage() || 'en'));
		}
	}
	this.init();
}
var languageSettingCallback = function(data) {
	TranslateService.prototype.languageSetting = data['language-setting'];
}
var translateMapCallback = function(data) {
	TranslateService.prototype.translateMap = data;
}
