(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http'];

    function Profile($http) {
        var Profile = {
            get: get,
            getAccount: getAccount,
            downloadGames: downloadGames

        };

        return Profile;

        function get(accountId) {
            return $http.get('/api/profiles/' + accountId);
        }

        function getAccount(accountId) {
            return $http.get("/api/accounts/" + accountId);
        }

        function downloadGames(accountId) {
            console.log("lol");
            $http.post("api/accounts/" + accountId + "/download");
        }
    }
})();