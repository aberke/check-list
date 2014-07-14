/*********************************************************************


	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014




AngularJS controllers 

*********************************************************************/

function MainCntl($scope, $window, $location, APIservice, UserFactory) {
	/* This controller's scope spans over all views */
	$scope.domain = $window.location.origin;
	$scope.user;
	var showingControls;
	var view;

	var resetControls = function() {
		showingControls = false;
		if (view) { view.className = ""; }
	}

	$scope.clickHamburger = function() {
		// DO get view again each time to ensure controls work

		view = document.getElementById('view');
		if (showingControls) {
			view.className = "";
			showingControls = false;
		} else {
			view.className = "collapsed";
			showingControls = true;
		}
	}

	var setupGoogleAnalytics = function() {
		// log every new page view in production

		if ($scope.domain == "http://clean-slate2.herokuapp.com") {
			$scope.$on('$routeChangeSuccess', function(event) {
				console.log('pushing to google-analytics')
				$window.ga('send', 'pageview', { page: $location.path() });
			});
		}
	}
	$scope.logout = function(){
		$scope.user = null;
		UserFactory.logout();
	}
	var resetUser = function() {
		$scope.user = null;
		UserFactory.GETuser().then(function(user) {
			$scope.user = user;
			console.log('user', user)
		});
	}
	var init = function() {
		setupGoogleAnalytics();
		$scope.$on('$routeChangeSuccess', function(event) {
			resetUser();
			resetControls();
		});
		document.getElementById('control-view').style.display = "block";
		showingControls = false;
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
		APIservice.GET('/api/cleaner/validate-new-phonenumber/' + phonenumber).then(successCallback, errorCallback);
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
			$location.path('/dashboard');
		}
		var errorCallback = function(message) {
			$scope.error.message = message;
		}
		APIservice.POST('/api/cleaner', $scope.cleaner).then(successCallback, errorCallback);
	}

	function init() {
		$scope.stage = 0;
		$scope.error = {};
		$scope.waiting = false;
		$scope.cleaner = {};
	}
	init();
}

function LoginCntl($scope, $location, APIservice, UserFactory) {

	$scope.cleaner = {};
	$scope.error = {};

	$scope.login = function() {
		$scope.error = {};
		var errorCallback = function(message) {
			$scope.error.message = message;
		}
		var successCallback = function(data) {
			$location.path('/dashboard'); 
		}
		UserFactory.login($scope.cleaner).then(successCallback, errorCallback);
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
		APIservice.POST("/auth/send-reset-code", $scope.cleaner).then(successCallback, errorCallback);
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
			$location.path('/dashboard');
		}
		APIservice.PUT("/auth/reset-password", $scope.cleaner).then(successCallback, errorCallback);
	}
}

function DashboardCntl($scope, $location, user, lists) {

	$scope.lists;

	$scope.newList = function() {
		console.log('newList')
		$location.path('/list/new');
	}

	$scope.selectList = function(list) {
		console.log('selectList', list)
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

function ListCntl($scope, TaskFactory, APIservice, user) {
	/* ListCntl passed the list object or null if this is a new list */
	console.log('user', user)
	var cleaner = user;
	var cleanerID = user._id;
	console.log('cleanerID', cleanerID)
	if (!cleanerID) { console.log('TODO');}
	$scope.rooms;
	$scope.list;
	$scope.editingListInfo;

	$scope.saveListInfo = function() {
		/* if no list._id -> new list, must POST (just the first time)
			else: PUT data
		*/
		$scope.editingListInfo = false;
	console.log('saveListInfo', $scope.list)

		var errorCallback = function(message) {
			console.log('ERROR on saveListInfo', message)
		}
		var successCallback = function(data) {
			console.log('successCallback', data)
			$scope.list._id = data._id;
		}

		if (!$scope.list._id) {
			APIservice.POST('/api/cleaner/' + cleanerID + '/list', $scope.list).then(successCallback, errorCallback);
		}
	}


	$scope.clickListInfo = function() {
		if ($scope.editingListInfo) {
			$scope.saveListInfo();
		} else {
			$scope.editingListInfo = true;
		}
	}

	$scope.clickRoom = function(room) {
		room.active = room.active ? false : true;
	}
	$scope.clickTask = function(room, task) {
		if (task.selected) {
			task.selected = false;
			room.taskCount -= 1;
		} else {
			task.selected = true;
			room.taskCount += 1;
		}
	}
	$scope.addCustomTask = function(room, newCustomTask) {
		room.taskObjs.push({
			'name': newCustomTask,
			'selected': true,
			'custom': true,
		});
		room.taskCount += 1;
	}
	$scope.sendList = function() {
		console.log('sendList')
		$scope.error = {};
		/* if still need to edit list info, force them to do so
			open up the list editing and scroll to top of the page where it is
		*/ 
		if (!($scope.list.phonenumber && $scope.list.location && $scope.list.name)) {
			$scope.editingListInfo = true;
			document.body.scrollTop = document.documentElement.scrollTop = 0;
			$scope.error.message = 'required...'
			return false;
		}
		var successCallback = function() {
			$scope.editingListInfo = false;
			$scope.confirmationSent = true;
		}

		// TODO -- MAKE PUT INSTEAD
		//APIservice.PUT('/api/list/send').then(successCallback, errorCallback);
		successCallback();
	}
	

	var init = function() {
		$scope.editingListInfo = false;

		$scope.list = {
			'rooms': [],
		};

		$scope.rooms = [{
			'name': 'LIVING ROOM',
			'type': 'livingroom',
			'taskCount': 0,
			'taskObjs': TaskFactory.defaultTaskObjs(),
			'tasks': [],
		},{
			'name': 'BED ROOM',
			'type': 'bedroom',
			'taskCount': 0,
			'taskObjs': TaskFactory.defaultTaskObjs(),
			'tasks': [],
		},{
			'name': 'BATH ROOM',
			'type': 'bathroom',
			'taskCount': 0,
			'taskObjs': TaskFactory.defaultTaskObjs(),
			'tasks': [],
		},{
			'name': 'KITCHEN',
			'type': 'kitchen',
			'taskCount': 0,
			'taskObjs': TaskFactory.defaultTaskObjs(),
			'tasks': [],
		},{
			'name': 'ADD ROOM',
			'type': 'etc',
			'taskCount': 0,
			'taskObjs': TaskFactory.defaultTaskObjs(),
			'tasks': [],
		},];
	}
	init();
}









