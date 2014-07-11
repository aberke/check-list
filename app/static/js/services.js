/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS app

****************************************************/


var FormService = function() {

}


var APIservice = function($http, $q){

  function HTTP(method, endpoint, data, params, options) {

    var config = {
      method:  method,
      url:    endpoint,
      data:   (data || {}),
      params: (params || {}),
    };
    options = (options || {})
    for (var opt in options) { config[opt] = options[opt]; }
    
    var deferred = $q.defer();
    $http(config)
    .success(function(returnedData){
      deferred.resolve(returnedData);
    })
    .error(function(errData, status) {
      console.log('API Error', status, errData.message);
      deferred.reject(errData.message || "Error");
    });
    return deferred.promise;
  };
  function upload(method, endpoint, files, successCallback, errorCallback) {
    var fd = new FormData();
    fd.append("file", files[0]); //Take the first selected file

    var options = {
        withCredentials: true,
        headers: {'Content-Type': undefined },
        transformRequest: angular.identity
    };
    return HTTP(method, endpoint, fd, null, options).then(successCallback, errorCallback);
  }

  /* ---------- below functions return promises --------------------------- 
                                              (route resolve needs promises) 
  */
  
  this.PUTupload = function(endpoint, files) {
    return upload('PUT', endpoint, files);
  }
  this.POSTupload = function(endpoint, files) {
    return upload('POST', endpoint, files);
  }

  this.GET = function(endpoint, data) { // if there's data, send it as params
    return HTTP('GET', endpoint, null, data);
  };
  this.POST = function(endpoint, data) {
    return HTTP('POST', endpoint, data);
  };
  this.PUT = function(endpoint, data) {
    return HTTP('PUT', endpoint, data);
  };
  this.DELETE = function(endpoint, data) {
    return HTTP('DELETE', endpoint, data);
  };

};

var AuthService = function($window, APIservice) {

  this.logout = function() {
    $window.location = "/auth/logout";
  }
  this.login = function(data) {
    return APIservice.POST('/auth/login', data);
  }
  this.GETuser = function() {
    return APIservice.GET('/auth/user');
  }

}


