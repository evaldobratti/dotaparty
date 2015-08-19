(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http'];

    function Profile($http) {
        var Profile = {
            get: get,
            getPlayersMatches: getPlayersMatches,
            getAccount: getAccount,
            downloadGames: downloadGames

        };

        return Profile;

        function get(accountId) {
            return $http.get('/api/profiles/' + accountId);
        }

        function getPlayersMatches(accountId, others) {
            return $http.get('/api/profiles/' + accountId + '?others=' + others.join(','));
        }

        function getAccount(accountId) {
            return $http.get("/api/accounts/" + accountId);
        }

        function downloadGames(accountId) {
            return $http.post("api/accounts/" + accountId + "/download");
        }
    }
})();