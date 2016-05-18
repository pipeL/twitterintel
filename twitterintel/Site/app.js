(function () {
    'use strict';
 
    angular
        .module('app', ['ngRoute', 'ngCookies'])
        .config(config)
        .directive('ngRedirectTo',ngRedirectTo)
        .run(run);
        
    ngRedirectTo.$inject =['$window']
    
    function ngRedirectTo($window) {
        return {
            restrict: 'A',
            link: function(scope, element, attributes) {
                element.bind('click', function (event) {
                    //assign ng-Redirect-To attribute value to location
                    $window.location.href = attributes.ngRedirectTo;
                });
            }
        };
    }
 
    config.$inject = ['$routeProvider', '$locationProvider'];
    function config($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                controller: 'HomeController',
                templateUrl: 'home/home.view.html',
                css: 'home/home.css',
                controllerAs: 'vm'
            })
 
            .when('/login', {
                controller: 'LoginController',
                templateUrl: 'login/login.view.html',
                controllerAs: 'vm'
            })
 
            .when('/register', {
                controller: 'RegisterController',
                templateUrl: 'register/register.view.html',
                controllerAs: 'vm'
            })
            .when('/start', {
                controller: 'StartController',
                templateUrl: 'start/start.view.html',
                controllerAs: 'vm'
            })
            .when('/rankingwords', {
                controller: 'RankingwordsController',
                templateUrl: 'rankingwords/rankingwords.view.html',
                controllerAs: 'vm'
            })
            .when('/topwordsgraphs', {
                controller: 'TopwordsgraphsController',
                templateUrl: 'topwordsgraphs/topwordsgraphs.view.html',
                css: 'topwordsgraphs/topwordsgraphs.css',
                controllerAs: 'vm'
            })
            .when('/instantfeed', {
                controller: 'InstantfeedController',
                templateUrl: 'instantfeed/instantfeed.view.html',
                controllerAs: 'vm'
            })
            .when('/topwordsgraphs2', {
                controller: 'TopwordsgraphsController2',
                templateUrl: 'topwordsgraphs2/topwordsgraphs.view.html',
                css: 'topwordsgraphs2/topwordsgraphs.css',
                controllerAs: 'vm'
            })
            .when('/topwordsgraphs3', {
                controller: 'TopwordsgraphsController3',
                templateUrl: 'topwordsgraphs3/topwordsgraphs.view.html',
                css: 'topwordsgraphs3/topwordsgraphs.css',
                controllerAs: 'vm'
            })
            .when('/exprimentar', {
                controller: 'ExprimentarController',
                templateUrl: 'exprimentar/exprimentar.view.html',
                controllerAs: 'vm'
            })
            .when('/tweets', {
                controller: 'TweetsController',
                templateUrl: 'tweets/tweets.view.html',
                controllerAs: 'vm'
            })
 
            .otherwise({ redirectTo: '/login' });
    }
 
    run.$inject = ['$rootScope', '$location', '$cookieStore', '$http'];
    function run($rootScope, $location, $cookieStore, $http) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            console.log('ola');
        }
        $rootScope.windowWidth = window.innerWidth;
            window.addEventListener('resize', function() {
                $rootScope.$apply(function() {
                    $rootScope.windowWidth = window.innerWidth;
                });
            });
        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in and trying to access a restricted page
            var restrictedPage = $.inArray($location.path(), ['/login', '/register']) === -1;
            var loggedIn = $rootScope.globals.currentUser;
            if (restrictedPage && !loggedIn) {
                $location.path('/login');
            }
        });
    }
 
})();