(function () {
    'use strict';

    angular
        .module('dotaparty.home.services')
        .factory('Home', Home);

    Home.$inject = ['$http'];

    function Home($http) {
        var Home = {
            find: find
        };

        return Home;

        function find(query) {
            return $http.get('api/find?query=' + query);
        }
    }
})();