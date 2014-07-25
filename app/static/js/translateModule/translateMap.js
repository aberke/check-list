/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS translateModule: translateMap

 	Contains the actual translation data in translateMap.
 	Translate data comes from a publicly published Google Spreadsheet
 	Script requesting JSON data from this sheet is attached to head of base.html
 	Initially contains empty map
 		on GETtranslateDataCallback: populates the map with translations

****************************************************/

var translateMap = {};

var GETtranslateDataCallback = function(data) {
	/* Callback for data returned from Google API via script tag attached in base.html 
		Parses returned object into translateMap

		@param {Object} data -- data object to parse into translateMap
	*/

	var entryList = data.feed.entry;
	var entry;
	var keyname;
	var content;
	var translationsArray;
	var translationPartition;
	for (var i=0; i<entryList.length; i++) {
		entry = entryList[i];

		keyname = entry.title['$t'];
		translateMap[keyname] = {};

		// content of form "en: phone, es: phonenumber abbr. in spanish"
		content = entry.content['$t'];
		translationsArray = content.split(/, */);

		for (var a=0; a<translationsArray.length; a++) {
			translationPartition = translationsArray[a].split(/: */);
			var language = translationPartition[0];
			var translation = translationPartition[1];

			translateMap[keyname][language] = translation;
		}
	}
	console.log('translateMap', translateMap)
}