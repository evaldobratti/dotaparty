(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http'];

    function Profile($http) {
        var Profile = {
            get: get,
            getFriends: getFriends,
            getPlayersMatches: getPlayersMatches,
            downloadGames: downloadGames,
            getReportsCreated: getReportsCreated,
            getReportsReceived: getReportsReceived,
            isAvailableToDownload: isAvailableToDownload
        };

        return Profile;

        function get(accountId) {
            return $http.get('/api/profiles/' + accountId);
        }

        function getFriends(accountId, others) {
            var othersPar = '';
            if (others != undefined || others != null) {
                othersPar = '?others=' + others.join(',');
            }

            return $http.get('/api/profiles/' + accountId + '/friends' + othersPar);
        }

        function getPlayersMatches(accountId, others) {
            return $http.get('/api/profiles/' + accountId + '?others=' + others.join(','));
        }

        function downloadGames(accountId) {
            return $http.post("api/profiles/" + accountId + "/download");
        }

        function getReportsCreated(accountId, elements_per_page, page, others) {
            var e = elements_per_page == undefined ? 4 : elements_per_page;
            var p = page == undefined ? 1 : elements_per_page;
            var o = others == undefined ? '': others.join(',');

            return $http.get('/api/profiles/' + accountId + '/reports/created?elements_per_page='+e+'&page='+p+'&others='+o);

        }

        function getReportsReceived(accountId, elements_per_page, page) {
            var e = elements_per_page == undefined ? 4 : elements_per_page;
            var p = page == undefined ? 1 : elements_per_page;

            return $http.get('/api/profiles/' + accountId + '/reports/received?elements_per_page='+e+'&page='+p);
        }

        function isAvailableToDownload(accountId) {
            return $http.get('/api/profiles/' + accountId + '/is_available_to_download');
        }
    }
})();