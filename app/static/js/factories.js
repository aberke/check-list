/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS app

****************************************************/


var TaskFactory = function() {
	/* used by the ListCntl to get tasks lists for the rooms */

	var defaultTasks = [
		'Vacuuming',
		'Fluff the pillows',
		'Polish something',
		'Arrange the things',
	];
	var tasks = [{
		'name': 'taskname',
		'selected': false,
		'custom': true,
	}];

	return {
		defaultTaskObjs: function() {
			var tasks = [];
			for (t in defaultTasks) {
				tasks.push({
					name: defaultTasks[t],
					selected: false,
					custom: false,
				});
			}
			return tasks;
		}
	}
}


var UserFactory = function($http, $q, $window, APIservice) {
	/* 
	Stores 
		{dict} user 	-- authenticated user or null if user logged out
		{list} lists 	-- the authenticated user's lists or null
		{dict} listsMap -- map of authenticated user's lists {_id: list} or null

	Provides login/logout utility which update the stored user as well
	*/
	var self = this;
	// following initialized in reset function
	var user;
	var lists;
	var listsMap;

	function reset() {
		user = undefined;
		lists = null;
		listsMap = null; // will be { list_id: list }
	}
	reset();

	function createListsMap(lists) {
		listsMap = {};
		var list;
		for (var i=0; i<lists.length; i++) {
			list = lists[i];
			listsMap[list._id] = list;
		}
		return listsMap;
	}


	function GETlists(tries) {
		/*
			@param {int|undefined} how many times this function has already been called
			Returns {promise} that will be resolved with {list} lists data

			If lists already stored, resolve promise right away, 
				otherwise GET authenticated user's lists
		*/
		var deferred = $q.defer();
		var promise = deferred.promise;
		
		if (lists) {
			deferred.resolve(lists);
			return promise;
		}

		// if user null and only 1st try - GET user and try again
		if (!user && !tries) {
			// chain current promise behind GETuser() promise -- let previous promise resolve after getting user
			promise = GETuser().then(function() { return GETlists(1); });
			return promise;
		}

		// if !user._id and 2nd try, then user must be logged out and there are no lists to get
		if (!user && tries) {
			deferred.resolve(lists);
			return promise;
		}

		APIservice.GET('/api/list/search?_cleaner=' + user._id).then(function(data) {
			lists = data;
			listsMap = createListsMap(lists);
			deferred.resolve(lists);
		});

		return promise;
	}

	function logout() {
		/* Redirect to be resolved to '/' by server */
		reset();
		$window.location = "/auth/logout";
	}

	function login(userData) {
		var deferred = $q.defer();
		if (user) {
			console.log('GETuser: already have user')
			deferred.resolve(user);
			return deferred.promise;
		}

		$http({method: 'POST', url: '/auth/login', data: userData})
			.success(function(data) {
				user = data;
				deferred.resolve(user);
			})
			.error(function(errData) {
				deferred.reject(errData.message || "Error");
			});

		return deferred.promise;
	}

	function GETuser() {
		/* Returns Promise */

		var deferred = $q.defer();
		if (user) {
			console.log('GETuser: already have user:', typeof user, user)
			deferred.resolve(user);
			return deferred.promise;
		}

		$http({method: 'GET', url: '/auth/user'})
			.success(function(data) {
				user = data;
				if (user == 'null') { user = null; }
				deferred.resolve(user);
			})
			.error(function(errData) {
				console.log('GET USER ERROR', errData);
				deferred.reject(errData.message || "Error");
			});
		return deferred.promise;
	}

	// initialize the user
	GETuser().then(function(data) {
		user = data;
		GETlists();
	});
	console.log('UserFactory')

	return {
		login: login,
		logout: logout,
		GETuser: GETuser,
		GETlists: GETlists,
	}
}