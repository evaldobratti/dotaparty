(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.services')
        .factory('DetailMatch', DetailMatch);

    DetailMatch.$inject = ['$http'];

    function DetailMatch($http) {
        var DetailMatch = {
            get: get
        };

        return DetailMatch;

        function get(matchId) {
            console.warn("doing get")
            return $http.get('/api/detailmatches/' + matchId);
        /*.then(registerSuccessFn, registerErrorFn);

            function registerSuccessFn(data, status, headers, config) {
                console.log(data.data);
                return data.data;
            }

            function registerErrorFn(data, status, headers, config) {
                console.error('Epic failure!');
           }*/
        }
    }
})();