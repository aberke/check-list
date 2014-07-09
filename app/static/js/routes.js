/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS app

****************************************************/


App.config(function($routeProvider) {

	$routeProvider
		.when('/', {
			templateUrl: '/static/html/partials/index.html',
		})
		.when('/new', {
			templateUrl: '/static/html/partials/new.html',
			controller: NewCntl,
		})
		.when('/test', {
			templateUrl: '/static/html/partials/test.html',
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
		})
		.when('/list/new', {
			templateUrl: '/static/html/partials/list-view.html',
			controller: ListCntl,
		})
		.when('/list/:id', {
			templateUrl: '/static/html/partials/list-view.html',
			controller: ListCntl,
		})
		.otherwise({
			redirectTo: '/'
		});
});







