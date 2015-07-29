(function () {
    'use strict';

    angular
        .module('dotaparty.friends.services')
        .factory('Friends', Friends);

    Friends.$inject = ['$http'];

    function Friends($http) {
        var Friends = {
            get: get,
            getPage: getPage
        };

        return Friends;

        function get(accountsIds) {
            return $http.get('/api/friends/' + accountsIds);
        }

        function getPage(accountsIds, page) {
            return $http.get('/api/friends/' + accountsIds + "?page=" + page);
        }
    }
})();