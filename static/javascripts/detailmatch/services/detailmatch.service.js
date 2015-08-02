(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('DetailMatch', DetailMatch);

    DetailMatch.$inject = ['$http'];

    function DetailMatch($http) {
        var DetailMatch = {
            get: get,
            getMatchesByAccountId: getMatchesByAccountId
        };

        return DetailMatch;

        function get(matchId) {
            return $http.get('/api/detailmatches/' + matchId);
        }

        function getMatchesByAccountId(accountId, page) {
            return $http.get('/api/detailmatches/account/' + accountId + "?page=" + page);
        }
    }
})();