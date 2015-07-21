(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http'];

    function Profile($http) {
        var Profile = {
            get: get,
            getAccount: getAccount
        };

        return Profile;

        function get(accountId) {
            return $http.get('/api/profiles/' + accountId);
        }

        function getAccount(accountId) {
            return $http.get("/api/accounts/" + accountId);
        }
    }
})();