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
            Profile.getAccount(vm.accountId).then(function (result) {
                vm.account = result.data;
            });

            Profile.get(vm.accountId).then(function (result) {
                vm.games = result.data;
                vm.games.friends = vm.games.friends.slice(0, Math.min(vm.games.friends.length, 12))
            });

            DetailMatch.getMatchesByAccountsIds(vm.accountId, vm.currentDetailMatchesPage).then(function (data) {
                vm.currentDetailMatchesPage += 1;
                vm.matches = vm.matches.concat(data.data.results);
            });
        }

        function downloadGames() {
            Profile.downloadGames(vm.account.account_id).
                success(function () {
                    $rootScope.alerts.push({
                        type: 'success',
                        msg: 'It will start to download your games'
                    });
                }).
                error(function () {
                    $rootScope.alerts.push({
                        type: 'danger',
                        msg: 'It was not possible to download your games due to an internal error.'
                    });
                });

        }
    }
})();