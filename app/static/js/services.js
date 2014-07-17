/***************************************************
	Significance Labs
	Brooklyn, NYC

 	Author: Alexandra Berke (aberke)
 	Written: June 2014


 	AngularJS app

****************************************************/

var UtilityService = function() {

  this.dateStringToDate = function(dateString) {
    /*
    Server returns datetimes as UTC strings like 2014-07-15 20:56:32.027186
    Safari fails to make a new Date out of these without extra help

    @param {string} dateString   - UTC string to turn into Date object
    Returns {Date obj}
    */
    if (dateString instanceof Date) { return; } // necessary to avoid errors when dateString is already turned into Date object
    
    var arr = dateString.split(/[- :]/);
    return new Date(arr[0], arr[1]-1, arr[2], arr[3], arr[4], arr[5]);
  }

  this.removeFromList = function(list, item, matchingKey) {
    /* 
    @param {array} list         - list from which to find and remove item
    @param {object} item        - object that presumably has matchingKey that is subject to removal
    @param {string} matchingKey - key on which to match items in list to item to find the item

    Returns {boolean} true if removed item, false otherwise
    */
    if (!(item && matchingKey && matchingKey in item)) {
      return false;
    }
    for (var i=0; i<list.length; i++) {
      if (list[i][matchingKey] == item[matchingKey]) {
        list.splice(i, 1);
        return true;
      }
    }
    return false;
  }

}


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
