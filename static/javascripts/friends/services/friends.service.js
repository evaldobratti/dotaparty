(function () {
    'use strict';

    angular
        .module('dotaparty.friends.services')
        .factory('Friends', Friends);

    Friends.$inject = ['$http'];

    function Friends($http) {
        var Friends = {
            get: get
        };

        return Friends;

        function get(accountId) {
            return $http.get('/api/profile/' + accountId);
        }
    }
})();