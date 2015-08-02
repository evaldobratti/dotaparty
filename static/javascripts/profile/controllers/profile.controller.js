(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$routeParams', 'Profile', 'DetailMatch'];

    function ProfileController($routeParams, Profile, DetailMatch) {
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
            });

            DetailMatch.getMatchesByAccountId(vm.accountId, vm.currentDetailMatchesPage).then(function (data) {
                vm.currentDetailMatchesPage += 1;
                vm.matches = vm.matches.concat(data.data.results);
                console.log(data.data.results);
            });
        }

        function downloadGames() {
            Profile.downloadGames(vm.account.account_id);
        }
    }
})();