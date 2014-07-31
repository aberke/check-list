/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014


 	AngularJS translateModule: service

****************************************************/

var TranslateService = function() {

	/*
	- Manager of current language {String} currentLanguage
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
	translateMap is constructed in translateMap.js
	*/


	var currentLanguage;
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

	this.getCurrentLanguage = function() {
		return currentLanguage;
	}
	this.setCurrentLanguage = function(language) {
		currentLanguage = language;
		return language;
	}
	this.translateMap = translateMap;

	this.translate = function(keyname) {
		/*
		@param {String} keyname -- keyname to look up in translate map and translate
		Returns translation found in translateMap or (untranslated) original keyname if no translation found
		*/
		if (keyname in translateMap) {
			return translateMap[keyname][currentLanguage];
		}
		return keyname;
	}

	var init = function() {
		// initialize currentLanguage to whichever language user's browser uses. 
		// defaults to english
		var detectedLanguage = detectLanguage();
		currentLanguage = (detectedLanguage || 'en');
	}
	init();
}
