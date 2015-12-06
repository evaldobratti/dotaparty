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
            downloadGames: downloadGames,
            getReportsCreated: getReportsCreated,
            getReportsReceived: getReportsReceived
        };

        return Profile;

        function get(accountId) {
            return $http.get('/api/profiles/' + accountId);
        }

        function getPlayersMatches(accountId, others) {
            return $http.get('/api/profiles/' + accountId + '?others=' + others.join(','));
        }

        function downloadGames(accountId) {
            return $http.post("api/profiles/" + accountId + "/download");
        }

        function getReportsCreated(accountId, elements_per_page, page) {
            var e = elements_per_page == undefined ? 4 : elements_per_page;
            var p = page == undefined ? 1 : elements_per_page;

            return $http.get('/api/profiles/' + accountId + '/reports/created?elements_per_page='+e+'&page='+p);
        }

        function getReportsReceived(accountId, elements_per_page, page) {
            var e = elements_per_page == undefined ? 4 : elements_per_page;
            var p = page == undefined ? 1 : elements_per_page;

            return $http.get('/api/profiles/' + accountId + '/reports/received?elements_per_page='+e+'&page='+p);
        }
    }
})();