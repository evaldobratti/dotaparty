(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$rootScope', '$routeParams', 'Profile', 'DetailMatch'];

    function ProfileController($rootScope, $routeParams, Profile, DetailMatch) {
        var vm = this;
        vm.accountId = $routeParams.accountId;
        vm.currentDetailMatchesPage = 1;
        vm.downloadGames = downloadGames;
        vm.matches = [];

        active();
        function active() {

            Profile.get(vm.accountId).then(function (result) {
                vm.account = result.data;
            });

            DetailMatch.getMatchesByAccountsIds(vm.accountId, vm.currentDetailMatchesPage).then(function (data) {
                vm.currentDetailMatchesPage += 1;
                vm.matches = data.data.results;

                determineVictoryOrLoss(vm.matches);
            });
        }

        function downloadGames() {
            if (vm.account.matches_download_required)
                return;

            Profile.downloadGames(vm.account.account_id).
                success(function () {
                    vm.account.matches_download_required = true;
                }).
                error(function () {
                    $rootScope.alerts.push({
                        type: 'danger',
                        msg: 'It was not possible to download your games due to an internal error.'
                    });
                });

        }

        function determineVictoryOrLoss(matches) {
            matches.forEach(function (match) {
                if (match.is_radiant_win)
                    match.match_won = match.radiant_team.length > 0;
                else
                    match.match_won = match.dire_team.length > 0;

            });
        }
    }
})();