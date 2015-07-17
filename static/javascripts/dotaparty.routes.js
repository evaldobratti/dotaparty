(function () {
    'use strict';

    angular
        .module('dotaparty.routes')
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider.when('/matches/:matchId', {
                controller: 'DetailMatchController',
                controllerAs: 'vm',
                templateUrl: 'static/templates/detailmatch.html'
            }
        ).when('/profiles/:accountId', {
            controller: 'ProfileController',
            controllerAs: 'vm',
            templateUrl: 'static/templates/profile.html'
        }).otherwise('/');
    }
})();