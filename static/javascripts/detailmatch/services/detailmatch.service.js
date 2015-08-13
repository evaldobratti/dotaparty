(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('DetailMatch', DetailMatch);

    DetailMatch.$inject = ['$http'];

    function DetailMatch($http) {
        var DetailMatch = {
            get: get,
            getMatchesByAccountsIds: getMatchesByAccountsIds
        };

        return DetailMatch;

        function get(matchId) {
            return $http.get('/api/detailmatches/' + matchId);
        }

        function getMatchesByAccountsIds(accountsIds, page) {
            return $http.get('/api/matches/accounts/' + accountsIds + "?page=" + page);
        }
    }
})();