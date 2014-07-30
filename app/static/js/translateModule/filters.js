/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS translateModule: filter

****************************************************/



function TranslateFilter(TranslateService) {

	/*
	Fed keynames to translate.
	Calls TranslateService to do the work of the translations
	If it gets back undefined or null (translation not found):
		returns keyname instead
	
	Optionally takes parameter format - converts to this format

	Use in an HTML file looks like: {{ 'KEY_NAME' | translate: 'uppercase' }}
	*/

	var convertToFormat = function(string, format) {
		switch (format) {
			case 'uppercase':
				string = string.toUpperCase();
				break;
			case 'titlecase':
				string = string.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
		}
		return string;
	}

	return function(keyname, format) {
		/*
		@param {string} keyname: keyname to translate
		@param {string} format (optional) ['uppercase', 'titlecase']: format to return translation in
		*/
		// safely exist case when there's filler text that must be translated, but it's later a Number
		if (typeof keyname != 'string') { return keyname; }

		var translation = (TranslateService.translate(keyname) || keyname);
		return convertToFormat(translation, format);
	}
}
