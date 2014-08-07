/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS app

****************************************************/

var GeolocationFactory = function($http) {
  
	var GOOGLE_API_KEY = "AIzaSyCJxQK1oDn4U3kbDIK-epf96ckze7fuSHQ";
	var GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json?";
	var nearestLocations = null;
	var result_type = "street_address|intersection|transit_station|train_station|bus_station|establishment|premise|subpremise|neighborhood";

	var formatLocationResults = function(rawResults) {
		/*
		@param {array} rawResults - array returned by Google Maps API to parse
		Returns array of format ['formatted_address' for each address in rawResults]
		*/
		var formattedResults = [];
		for (var i=0; i<rawResults.length; i++) {
			var formattedAddress = rawResults[i].formatted_address;
			formattedResults.push(formattedAddress);
		}
		return formattedResults;
	}

  	var getNearestLocations = function(successCallback, errorCallback) {
  		/* 
  		Retrieves and formats array or nearest locations
  		
  		@param {function} successCallback - function to call with formatted results array on success
  		@param {function} errorCallback   - function to call on error with message
  		*/
	  	if (nearestLocations) { return successCallback(nearestLocations); }

	  	if (!navigator.geolocation) {
	  		return errorCallback("Browser doesn't support Geolocation");
	  	}
		navigator.geolocation.getCurrentPosition(function(position) {
			$http.get(GOOGLE_GEOCODE_URL + 'latlng=' + position.coords.latitude + ',' + position.coords.longitude + '&result_type=' + result_type + '&key=' + GOOGLE_API_KEY)
				.success(function(res) {
					nearestLocations = formatLocationResults(res.results);
					return successCallback(nearestLocations);
				})
				.error(function(errData) {
					console.log(errData);
					errorCallback('ERROR with reverse geocoding request');
				});

		}, function() {
			errorCallback("Browser doesn't support Geolocation");
		});
	}
	getNearestLocations(function() {});

	return {
		getNearestLocations: getNearestLocations,
	}
}

var TaskFactory = function($http) {
	/* used by the ListCntl to get tasks lists for the rooms */

	var defaultTasksLists; // maps { room_type: applicable default tasks }

	var GETdefaultTasks = function(callback) {
		$http.get('/static/data/default-tasks.json')
	       .then(function(res){
	          defaultTasksLists = res.data;
	          if (callback) { callback(); }          
	        });
	}
	GETdefaultTasks();


	var generateDefaultTask = function(name, type) {
		return { 
			'name': name,
			'room_type': (type || 'all'),
			'selected': false,
			'custom': false,
			'default': true,
		};
	};
	var generateCustomTask = function(name, type) {
		return {
			'name': name,
			'room_type': (type || 'all'),
			'selected': true,
			'custom': true,
			'default': false,
		}
	}

	var mergeDefaultTasks = function(tasksList, tasksMap, room_type, secondTry) {
		// possible GETdefaultTasks hasn't yet returned - if not, wait for it and make secondTry
		// only allow 2 tries because if 2nd try fails that means BAD data was returned
		if (!defaultTasksLists) {
			if (!secondTry) { 
				GETdefaultTasks(function() {
					mergeDefaultTasks(tasksList, tasksMap, room_type, true);
				});
			}
			return;
		}

		if (! (room_type && room_type in defaultTasksLists)) {
			return;
		}
		var task;

		// add the default tasks in
		var defaultList = defaultTasksLists[room_type]; 
		for (var i=0; i<defaultList.length; i++) {
			if (defaultList[i] in tasksMap) {
				continue;
			}
			task = generateDefaultTask(defaultList[i], room_type)
			tasksList.push(task);
			tasksMap[task.name] = task;
		}
	}

	var setupRoomsTasks = function(rooms) {
		/*
		@param {List of objects} rooms
			List of room objects that may or may not already have saved tasks
		
		Returns {List of objects} updated rooms list with added unselected tasks

		The main function called by Controller
		ListCntl passes in rooms to be filled in with default tasks
		Calls mergeDefaultTasks as a helper function
		*/
		for (var i=0; i<rooms.length; i++) {

			var tasksList = rooms[i].tasks;
			var tasksMap = {};
			var t;
			for (var j=0; j<tasksList.length; j++) {
				t = tasksList[j];
				tasksMap[t.name] = t;
			}

			// add the default tasks in
			mergeDefaultTasks(tasksList, tasksMap, 'all');
			// add in tasks specific to room_type
			mergeDefaultTasks(tasksList, tasksMap, rooms[i].type);

			rooms[i].tasks = tasksList;
		}
		return rooms;
	}

	return {
		generateCustomTask: generateCustomTask,
		setupRoomsTasks: setupRoomsTasks,
	}
}


var UserFactory = function($http, $q, $window, APIservice, UtilityService) {
	/* 
	Stores 
		{dict} user 	-- authenticated user or null if user logged out
		{list} lists 	-- the authenticated user's lists or null
		{dict} listsMap -- map of authenticated user's lists {_id: list} or null

	Provides login/logout utility which update the stored user as well
	*/

	// the following are initialized in reset function
	var user;
	var lists;
	var listsMap;

	function reset() {
		user = undefined;
		lists = null;
		listsMap = null; // will be { list_id: list }
	}
	reset();

	function removeList(list) {
		if (! (listsMap && lists && list._id in listsMap)) { return; }
		
		// remove from listsMap
		delete listsMap[list._id];
		
		// remove from lists
		UtilityService.removeFromList(lists, list, '_id');
	}

	function addList(list) {
		/* Used in Dashboard Cntl NewList function
			As soon as that list is POSTed, want to GET it
		*/
		if (!listsMap || !lists) {
			// not saving any time anyhow -- will just have to GET again later
			return;
		}
		list.last_modified = new Date();
		lists.push(list);
		listsMap[list._id] = list;
	}

	function GETlist(listID, tries) {
		var deferred = $q.defer();
		var promise = deferred.promise;
		
		if (listsMap) {
			deferred.resolve(listsMap[listID]);
			return promise;
		}
		if (tries) {
			deferred.reject(null);
			console.log('ERROR in GETlist -- TODO: handle');
			return promise;
		}
		promise = GETlists().then(function() { return GETlist(listID, 1); });
		return promise;

	}

	function setupLists(ls) {
		lists = [];
		listsMap = {};
		var list;
		for (var i=0; i<ls.length; i++) {
			list = ls[i];
			// turn last_modified date strings into date objects
			list.last_modified = UtilityService.dateStringToDate(list.last_modified);
			
			// turn feedback.date into date objects for each feedback in list.feedbacks
			for (var f=0; f<list.feedbacks.length; f++) {
				var feedback = list.feedbacks[f];
				feedback.date = UtilityService.dateStringToDate(feedback.date);
			}

			lists.push(list);
			listsMap[list._id] = list;
		}
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
			setupLists(data);
			deferred.resolve(lists);
		});

		return promise;
	}

	function logout() {
		/* Import that logout performed with a POST due to mobile browsers' aggressive caching */
		reset();
		$http({ method: 'POST', url: '/auth/logout' })
			.success(function() { $window.location = "/"; })
			.error(function(errData) { console.log('ERROR logging out -- TODO', errData); });
	}

	function login(userData) {
		var deferred = $q.defer();
		if (user) {
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

	return {
		login: login,
		logout: logout,
		GETuser: GETuser,

		addList: addList,
		GETlist: GETlist,
		GETlists: GETlists,
		removeList: removeList,
	}
}