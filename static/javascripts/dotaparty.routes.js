(function () {
    'use strict';

    var app = angular
        .module('dotaparty.routes');
    app.config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider.when('/matches/:matchId', {
            controller: 'DetailMatchController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/detailmatch.html'
        }).when('/profiles/:accountId', {
            controller: 'ProfileController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/profile.html'
        }).when('/friends/:accountIds', {
            controller: 'FriendsController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/friends.html'
        }).when('/', {
            controller: 'HomeController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/home.html'
        }).when('/status', {
            controller: 'StatusController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/status.html'
        }).otherwise('/');
    }
})();