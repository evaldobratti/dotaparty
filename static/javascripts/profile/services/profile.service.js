(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http'];

    function Profile($http) {
        var Profile = {
            get: get
        };

        return Profile;

        function get(accountId) {
            return $http.get('/api/profile/' + accountId);
        }
    }
})();