(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController );

    LoginController.$inject = ['$location', 'AuthenticationService', '$rootScope'];
    function LoginController($location, AuthenticationService, $rootScope) {
        var vm = this;

        vm.login = login;

        (function initController() {
            // reset login status
            AuthenticationService.ClearCredentials();
        })();

        function login() {
            vm.dataLoading = true;
            AuthenticationService.Login(vm.username, vm.password, function (response) {
                if (response.success) {
                    AuthenticationService.SetCredentials($rootScope.id,$rootScope.status,$rootScope.intel,vm.username, vm.password);
                    $location.path('/start');
                } else {
                    vm.dataLoading = false;
                    alert(response.message);
                }
            });
        };
    }

})();