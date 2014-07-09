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


// NOT USED
var UserFactory = function($http, $q, $rootScope, $location, APIservice) {
	console.log('UserFactory')
	/* consumers call 
						UserFactory.then(function(userData) {
							check userData isn't null
						})
	*/

	var deferred = $q.defer();
	$http({method: 'GET', url: '/auth/user'})
	.success(function(data) {
		if (!data.twitter_id) { data = null; }
		deferred.resolve(data);
	})
	.error(function(errData) {
		console.log('GET USER ERROR', errData);
		deferred.reject(errData);
	});

	return deferred.promise;
}