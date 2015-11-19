(function () {
    'use strict';

    angular
        .module('dotaparty.community.services')
        .factory('Community', Community);

    Community.$inject = ['$http'];

    function Community($http) {
        var Community = {
            submitNewReport: submitNewReport
        };

        return Community;

        function submitNewReport(reportedAccountId, reason, matchId) {
            return $http.post("api/community/report/", {
                reported: reportedAccountId,
                reason: reason,
                matchId: matchId
            });
        }
    }
})();