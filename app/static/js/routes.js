/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


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
				editMode: function() { return false; },
			},
		})
		.when('/list/:id/edit', {
			templateUrl: '/static/html/partials/list-view.html',
			controller: ListCntl,
			resolve: {
				user: userOrRedirect,
				list: function(UserFactory, $route) {
					return UserFactory.GETlist($route.current.params.id).then(function(list) {
						return list;
					});
				},
				editMode: function() { return true; },
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
		.when('/list/:id/client', { // TODO - TAKE OUT?
			templateUrl: '/static/html/partials/list-view.html',
			controller: ClientListCntl,
			resolve: {
				list: function(APIservice, $route, $location) {
					return APIservice.GET('/api/list/' + $route.current.params.id).then(function(list) {
						if (!list) { $location.path('/'); }
						return list;
					});
				},
			},
		})
		.otherwise({
			redirectTo: '/'
		});
});







