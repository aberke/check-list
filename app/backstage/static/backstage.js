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
					$scope.loading = false;
				})
				.error(function(errData) { $scope.error = errData; });


		}
		init();
	});














