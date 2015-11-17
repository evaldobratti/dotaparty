(function () {
    'use strict';

    angular
        .module('dotaparty.community.controllers')
        .controller('NewReportController', NewReportController);

    NewReportController.$inject = ['$rootScope', '$scope', 'Community', 'reportedPlayer'];

    function NewReportController($rootScope, $scope, Community, reportedPlayer) {
        var vm = this;
        vm.reportedPlayer = reportedPlayer;
        vm.submit = submit;

        function submit() {
            Community.submitNewReport(reportedPlayer.account_id, vm.reason)
                .error(function () {
                    console.log("erro");
                    $rootScope.alerts.push({
                        type: 'danger',
                        msg: 'It was not possible to download your games due to an internal error.'
                    });

                });
            $scope.closeThisDialog();

        }

    }
})();