(function () {
    'use strict';
 
    angular
        .module('app')
        .factory('UserService', UserService);
 
    UserService.$inject = ['$timeout', '$filter', '$q'];
    function UserService($timeout, $filter, $q) {
 
        var service = {};
 
        service.GetAll = GetAll;
        service.GetById = GetById;
        service.GetByUsername = GetByUsername;
        service.Create = Create;
        service.Update = Update;
        service.Delete = Delete;
 
        return service;
 
        function GetAll() {
            var deferred = $q.defer();
            deferred.resolve(getUsers());
            return deferred.promise;
        }
 
        function GetById(id) {
            var deferred = $q.defer();
            var filtered = $filter('filter')(getUsers(), { id: id });
            var user = filtered.length ? filtered[0] : null;
            deferred.resolve(user);
            return deferred.promise;
        }
 
        function GetByUsername(username) {
            var deferred = $q.defer();
            var filtered = $filter('filter')(getUsers(), { username: username });
            var user = filtered.length ? filtered[0] : null;
            deferred.resolve(user);
            return deferred.promise;
        }
 
        function Create(user) {
            var deferred = $q.defer();
            var response;
            var send = new Array();     
            send[0]=user.username;
            send[1]=user.firstname;
            send[2]=user.lastname;
            send[3]=user.password;
            send[4]=user.key;
            send[5]=user.consumer_key;
            send[6]=user.consumer_secret;
            send[7]=user.access_token;
            send[8]=user.access_token_secret;
                var response;
            
                    $.ajax({
                              type: "GET",
                              crossDomain: true,
                              data: {id:JSON.stringify(send)},
                              url: "http://89.155.219.76:80/Register",
                              dataType: "json",
                              success: function(result){
                                     if(result['0']=="True"){
                                         response = {success : true}
                                     }
                                     if (result['0']=="False")
                                         {
                                            response = {success : false} 
                                         }
                                     if (result['0']=="UserExist")
                                         {
                                            alert('UserExist')
                                            response = {success : false} 
                                         }
                                    deferred.resolve(response);
                                
                                    
                              }
                        
                      });
 
 
            return deferred.promise;
        }
 
        function Update(user) {
            var deferred = $q.defer();
 
            var users = getUsers();
            for (var i = 0; i < users.length; i++) {
                if (users[i].id === user.id) {
                    users[i] = user;
                    break;
                }
            }
            setUsers(users);
            deferred.resolve();
 
            return deferred.promise;
        }
 
        function Delete(id) {
            var deferred = $q.defer();
 
            var users = getUsers();
            for (var i = 0; i < users.length; i++) {
                var user = users[i];
                if (user.id === id) {
                    users.splice(i, 1);
                    break;
                }
            }
            setUsers(users);
            deferred.resolve();
 
            return deferred.promise;
        }
 
        // private functions
 
        function getUsers() {
            if(!localStorage.users){
                localStorage.users = JSON.stringify([]);
            }
 
            return JSON.parse(localStorage.users);
        }
 
        function setUsers(users) {
            localStorage.users = JSON.stringify(users);
        }
    }
})();
