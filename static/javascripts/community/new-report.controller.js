(function () {
    'use strict';

    angular
        .module('dotaparty.community.controllers')
        .controller('NewReportController', NewReportController);

    NewReportController.$inject = ['$rootScope', '$scope', 'Community', 'Snackbar', 'reportedPlayer', 'matchId'];

    function NewReportController($rootScope, $scope, Community, Snackbar, reportedPlayer, matchId) {
        var vm = this;
        vm.reportedPlayer = reportedPlayer;
        vm.matchId = matchId;
        vm.submit = submit;

        function submit() {
            Community.submitNewReport(reportedPlayer.account_id, vm.reason, vm.matchId)
                .then(onSuccess, onError);

            $scope.closeThisDialog();
        }

        function onSuccess(data){
            Snackbar.show('Report created successfully');
        }

        function onError(data){
            Snackbar.error('An error has occurred.' + data.data.error);
        }

    }
})();