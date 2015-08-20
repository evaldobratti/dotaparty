(function () {
    'use strict';

    angular
        .module('dotaparty.config')
        .config(config)
        .run(run);

    run.$inject = ['$http'];
    config.$inject = ['$locationProvider', 'cfpLoadingBarProvider'];

    function config($locationProvider, cfpLoadingBarProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');

        cfpLoadingBarProvider.includeSpinner = false;
    }

    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();