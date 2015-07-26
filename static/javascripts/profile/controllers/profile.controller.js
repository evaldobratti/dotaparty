(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$routeParams', 'Profile'];

    function ProfileController($routeParams, Profile) {
        var vm = this;
        vm.downloadGames = downloadGames;

        active();

        function active() {
            var accountId = $routeParams.accountId;
            Profile.getAccount(accountId).then(function(result) {
                vm.account = result.data;
            });

            Profile.get(accountId).then(function(result){
               vm.games = result.data;
            });
        }

        function downloadGames() {
            Profile.downloadGames(vm.account.account_id);
        }
    }
})();