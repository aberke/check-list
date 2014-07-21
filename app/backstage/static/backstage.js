/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014


 	backstage.js 

****************************************************/



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
						*/
						cleaner.last_active = new Date(cleaner.last_modified);
						for (var j=0; j<cleaner.lists.length; j++) {
							cleaner.lists[j].last_modified = new Date(cleaner.lists[j].last_modified);
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














