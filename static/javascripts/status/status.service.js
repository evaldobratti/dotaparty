(function () {
    'use strict';

    angular
        .module('dotaparty.status.services')
        .factory('Status', Status);

    Status.$inject = ['$http'];

    function Status($http) {
        var Status = {
            get: get
        };

        return Status;

        function get() {
            return $http.get('/api/statistics/');
        }

    }
})();