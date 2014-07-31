/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: Summer 2014


 	AngularJS app

****************************************************/


ChecklistApp.config(function($routeProvider) {

	var userOrRedirect = function(UserFactory, $location) {
		return UserFactory.GETuser().then(function(user) {
			if (!user) { /* user isn't logged in - redirect to home */
				$location.path('/');
			}
			return user; /* success: return user object */
		});
	};

	$routeProvider

		/*- cleaner views ----------------------------------------------*/
		.when('/', {
			templateUrl: '/static/html/partials/index.html',
		})
		.when('/new', {
			templateUrl: '/static/html/partials/new.html',
			controller: NewCntl,
		})
		.when('/sign-in', {
			templateUrl: '/static/html/partials/sign-in.html',
			controller: LoginCntl,
		})
		.when('/reset-password', {
			templateUrl: '/static/html/partials/reset-password.html',
			controller: ResetPasswordCntl,
		})
		.when('/dashboard', {
			templateUrl: '/static/html/partials/dashboard-view.html',
			controller: DashboardCntl,
			resolve: {
				user: userOrRedirect,
				lists: function(UserFactory) {
					return UserFactory.GETlists().then(function(lists) {
						return lists;
					});
				},
			},
		})
		.when('/list/:id/clean', {
			templateUrl: '/static/html/partials/list-clean-view.html',
			controller: ListCntl,
			resolve: {
				user: userOrRedirect,
				list: function(UserFactory, $route) {
					return UserFactory.GETlist($route.current.params.id).then(function(list) {
						return list;
					});
				},
			},
		})
		.when('/list/:id', {
			templateUrl: '/static/html/partials/list-view.html',
			controller: ListCntl,
			resolve: {
				user: userOrRedirect,
				list: function(UserFactory, $route) {
					return UserFactory.GETlist($route.current.params.id).then(function(list) {
						return list;
					});
				},
			},
		})
		/*---------------------------------------------- cleaner views -*/

		/*- client views -----------------------------------------------*/
		.when('/list/:id/agreement', {
			templateUrl: '/static/html/partials/list-agreement-view.html',
			controller: ListCntl,
			resolve: {
				list: function(APIservice, UtilityService, $route) {
					return APIservice.GET('/api/list/' + $route.current.params.id + '?populate_cleaner=true').then(function(list) {
						if (!list) { $location.path('/'); }
						list.last_modified = UtilityService.dateStringToDate(list.last_modified);
						return list;
					});
				},
				user: function() { return null; },
			},
		})
		.when('/receipt/:id', {
			templateUrl: '/static/html/partials/receipt-view.html',
			controller: ReceiptCntl,
			resolve: {
				receipt: function(APIservice, $route, $location) {
					return APIservice.GET('/api/receipt/' + $route.current.params.id).then(function(receipt) {
						if (!receipt) { $location.path('/'); }
						return receipt;
					});
				},
			},
		})
		/*------------------------------------------------------- client views -*/

		.otherwise({
			redirectTo: '/'
		});
});







