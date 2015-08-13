(function () {
    'use strict';

    angular
        .module('dotaparty.friends.services')
        .factory('Friends', Friends);

    Friends.$inject = ['$http'];

    function Friends($http) {
        var Friends = {
        };

        return Friends;

    }
})();