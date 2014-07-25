/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS translateModule: service

****************************************************/

var TranslateService = function() {

	// initialize currentLanguage to english
	var currentLanguage = 'en';

	this.getCurrentLanguage = function() {
		return currentLanguage;
	}
	this.setCurrentLanguage = function(language) {
		currentLanguage = language;
	}

	/*
	Keeps translations in translateMap:
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
	this.translateMap = translateMap;

	this.translate = function(keyname) {
		if (keyname in translateMap) {
			return translateMap[keyname][currentLanguage];
		}
		return null;
	}
}
