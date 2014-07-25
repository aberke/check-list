/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014


 	AngularJS translateModule
 	Separate module that main app module can depend on for translations

 	Architecture influenced by blogpost: http://blog.trifork.com/2014/04/10/internationalization-with-angularjs/


****************************************************/



var translateModule = angular.module('translateModule', [])

	.config(function($provide, $filterProvider) {

		// register services
		$provide.service('TranslateService', TranslateService);

		// register filters
		$filterProvider.register('translate', TranslateFilter);

	});







