(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['UserService', 'AuthenticationService' , '$location','$rootScope'];
    function HomeController(UserService, AuthenticationService, $location, $rootScope) {
        var vm = this;

        vm.user = null;
        vm.allUsers = [];
        vm.clearCredentials=clearCredentials;
        vm.deleteUser = deleteUser;

        initController();

        function initController() {
            loadCurrentUser();
            loadAllUsers();
        }

        function loadCurrentUser() {
            UserService.GetByUsername($rootScope.globals.currentUser.username)
                .then(function (user) {
                    vm.user = user;
                });
        }

        function loadAllUsers() {
            UserService.GetAll()
                .then(function (users) {
                    vm.allUsers = users;
                });
        }
        function clearCredentials(){
            AuthenticationService.ClearCredentials();
            $location.path('/#');
        }

        function deleteUser(id) {
            UserService.Delete(id)
            .then(function () {
                loadAllUsers();
            });
        }
    }

})();