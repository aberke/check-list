/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014


 	backstage.js 

****************************************************/

var localDateFromUTCstring = function(UTCstring) {
	/*
	@param {string} UTCstring -- string (assumed to be UTC time) to convert to a locale aware Date object
	Returns {Date} locale aware date object
	*/
	if (typeof UTCstring != 'string') { return UTCstring; }

	// must append ' UTC' to end of UTCstring and then create date object -- new Date function will then be locale aware
	var toAppend = ' UTC';
	if (UTCstring.substr(UTCstring - toAppend.length) != toAppend) {
		UTCstring = UTCstring + toAppend;
	}
	return new Date(UTCstring);
}


var App = angular.module('BackstageApp', [])

	.config(function($locationProvider) {

		$locationProvider.html5Mode(true);

	})


	.controller('MainController', function($scope, $http) {

		$scope.loading;
		$scope.cleaners;
		$scope.error;
		
	

		var init = function() {
			$scope.loading = true;


			$http({ method: 'GET', url: '/backstage/data/all' })
				.success(function(data) { 
					console.log('data', data)
					$scope.cleaners = data;

					// while waiting for DOM to render, minipulate data
					var cleaner;
					for (var i=0; i<$scope.cleaners.length; i++) {
						cleaner = $scope.cleaners[i];
						/* Sorting cleaners in ng-repeat by last_activity
							where last_activity is more recent of 
							cleaner.last_modified and 
							most recent of their lists last_modified

							Want to show locale aware dates, so using localDateFromUTCstring helper function
						*/

						// set cleaner.last_active as date object constructed from last_modified
						// default to June for backwards compatibility - first few cleaners not stamped with last_modified
						cleaner.last_active = cleaner.last_modified ? localDateFromUTCstring(cleaner.last_modified) : new Date(2014, 6, 1);

						for (var j=0; j<cleaner.lists.length; j++) {

							cleaner.lists[j].last_modified = localDateFromUTCstring(cleaner.lists[j].last_modified);

							if (cleaner.lists[j].last_modified > cleaner.last_active) {
								cleaner.last_active = cleaner.lists[j].last_modified;
							}
						}
					}
					$scope.loading = false;
				})
				.error(function(errData) { $scope.error = errData; });


		}
		init();
	});














