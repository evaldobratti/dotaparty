(function () {
    'use strict';

    var app = angular
        .module('dotaparty.routes');
    app.config(config);

    config.$inject = ['$stateProvider', '$urlRouterProvider'];

    function config($stateProvider, $urlRouterProvider) {
        $stateProvider.state('match ', {
            url: '/matches/:matchId',
            controller: 'DetailMatchController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/detailmatch.html'
        }).state('profile', {
            url: '/profiles/:accountId',
            controller: 'ProfileController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/profile.html',
            reloadOnSearch: false
        }).state('friends', {
            url: '/friends/:accountIds',
            controller: 'FriendsController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/friends.html'
        }).state('home', {
            url: '/',
            controller: 'HomeController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/home.html'
        }).state('status', {
            url: '/status',
            controller: 'StatusController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/status.html'
        }).state('error', {
            url: '/error',
            template: '<div>afff</div>'
        });

        $urlRouterProvider.otherwise("/");

    }
})();