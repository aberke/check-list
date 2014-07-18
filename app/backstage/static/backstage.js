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

		$scope.$on('$viewContentLoaded', function() {
			console.log('$viewContentLoaded')
		});
		
	

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
						for (var j=0; j<cleaner.lists.length; j++) {
							cleaner.lists[j].last_modified = new Date(cleaner.lists[j].last_modified);
						}
					}
					$scope.loading = false;
				})
				.error(function(errData) { $scope.error = errData; });


		}
		init();
	});














