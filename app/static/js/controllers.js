/*********************************************************************


	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014




AngularJS controllers 

*********************************************************************/

function MainCntl($scope, $window, $location, APIservice, AuthService) {
	/* This controller's scope spans over all views */
	$scope.domain = $window.location.origin;
	$scope.user = null;

	var setupGoogleAnalytics = function() {
		// log every new page view in production
		console.log('domain', $scope.domain)

		if ($scope.domain == "http://clean-slate.herokuapp.com") {
			$scope.$on('$routeChangeSuccess', function(event) {
				console.log('pushing to google-analytics')
				$window.ga('send', 'pageview', { page: $location.path() });
			});
		}
	}
	$scope.logout = function(){
		$scope.user = null;
		AuthService.logout();
	}
	var resetUser = function() {
		$scope.user = null;
		AuthService.GETuser().then(function(user) {
			if (user && user != "null") {
				$scope.user = user;
			}
			console.log('user', user)
		});
	}
	var init = function() {
		setupGoogleAnalytics();
		$scope.$on('$routeChangeSuccess', function(event) {
			resetUser();
		});
	}
	init();
}


function NewCntl($scope, $location, APIservice) {

	//$scope.showAll = true; // true iff testing

	$scope.error;
	$scope.waiting;
	$scope.cleaner;
	$scope.stage;

	$scope.submitPhonenumber = function() {
		// clear out old error
		$scope.error = {};
		// show waiting
		$scope.waiting = true;
		/* ensure that phonenumber is new and valid (sends SMS message via twilio)
			if not: err
			if so: increment stage appropriately
		*/
		var phonenumber = $scope.cleaner.phonenumber;
		if (!phonenumber) {
			$scope.waiting = false;
			$scope.error.phonenumber = true;
			return;
		}

		var successCallback = function() {
			$scope.waiting = false;
			$scope.stage = 1;
		}
		var errorCallback = function(message) {
			$scope.waiting = false;
			$scope.error.message = message;
			$scope.error.phonenumber = true;
		}
		APIservice.GET('/cleaner/validate-new-phonenumber/' + phonenumber).then(successCallback, errorCallback);
	}

	$scope.submitPassword = function() {
		/* POSTs new user */

		// clear old error
		$scope.error = {};

		if (!$scope.cleaner.password) {
			$scope.error.password = true;
		}
		if (!$scope.cleaner.confirmPassword || $scope.cleaner.confirmPassword != $scope.cleaner.password) {
			$scope.error.confirmPassword = true;
		}
		if ($scope.error.phonenumber||$scope.error.password||$scope.error.confirmPassword) {
			return false;
		}
		var successCallback = function(data) {
			console.log('new cleaner', data)
			$location.path('/lists');
		}
		var errorCallback = function(message) {
			$scope.error.message = message;
		}
		APIservice.POST('/cleaner', $scope.cleaner).then(successCallback, errorCallback);
	}

	function init() {
		$scope.stage = 0;
		$scope.error = {};
		$scope.waiting = false;
		$scope.cleaner = {};
	}
	init();
}

function LoginCntl($scope, $rootScope, $location, APIservice, AuthService) {

	$scope.cleaner = {};
	$scope.error = {};

	$scope.login = function() {
		$scope.error = {};
		var errorCallback = function(message) {
			$scope.error.message = message;
		}
		var successCallback = function(data) {
			$rootScope.user = data;
			$location.path('/lists'); 
		}
		AuthService.login($scope.cleaner).then(successCallback, errorCallback);
	}
}

function ResetPasswordCntl($scope, $timeout, $location, APIservice) {

	$scope.error = {};
	$scope.stage = 0;
	$scope.cleaner = {};
	$scope.sendAgainEnabled = true;

	$scope.sendResetCode = function() {
		/* send the reset code and hide send-again button for enough seconds to recieve SMS */
		$scope.error = {};
		$scope.sendAgainEnabled = false;
		$timeout(function() {
			$scope.sendAgainEnabled = true;
		}, 6000);

		var errorCallback = function(message) {
			$scope.error.message = message;
		}
		var successCallback = function(data) {
			$scope.stage = 1;
		}
		APIservice.POST("/cleaner/auth/send-reset-code", $scope.cleaner).then(successCallback, errorCallback);
	}
	$scope.submitNewPassword = function() {
		// clear old error
		$scope.error = {};

		if (!$scope.cleaner.reset_code) {
			$scope.error.reset_code = true;
		}
		if (!$scope.cleaner.password) {
			$scope.error.password = true;
		}
		if (!$scope.cleaner.confirmPassword || $scope.cleaner.confirmPassword != $scope.cleaner.password) {
			$scope.error.confirmPassword = true;
		}
		if ($scope.error.password||$scope.error.confirmPassword) {
			return false;
		}

		var errorCallback = function(message) {
			$scope.error.message = message;
		}
		var successCallback = function(data) {
			console.log('successCallback', data)
			$location.path('/profile/' + $scope.cleaner.phonenumber);
		}
		APIservice.PUT("/cleaner/auth/reset-password", $scope.cleaner).then(successCallback, errorCallback);
	}
}

function ListsCntl($scope) {

	$scope.lists;

	$scope.newList = function() {
		console.log('newList')
	}

	$scope.viewList = function() {
		console.log('viewList')
	}

	var init = function() {

		$scope.lists = [{
			'name': 'BOB’S HOUSE',
			'last_modified': '07/07/07',
		},{
			'name': 'AIRBNB #1',
			'last_modified': '07/07/07',
		},{
			'name': 'AIRBNB #2',
			'last_modified': '07/07/07',
		},];
	}
	init();
}

function RoomsCntl($scope) {

	$scope.rooms;


	

	var init = function() {

		$scope.rooms = [{
			'name': 'LIVING ROOM',
			'type': 'livingroom',
		},{
			'name': 'BED ROOM',
			'type': 'bedroom',
		},{
			'name': 'BATH ROOM',
			'type': 'bathroom',
		},{
			'name': 'KITCHEN',
			'type': 'kitchen',
		},{
			'name': 'EXTRA',
			'type': 'etc',
		},];
	}
	init();
}









