(function () {
    'use strict';

    angular
        .module('dotaparty.friends.controllers')
        .controller('FriendsController', FriendsController);

    FriendsController.$inject = ['$routeParams', 'DetailMatch', 'Profile'];

    function FriendsController($routeParams, DetailMatch, Profile) {
        var vm = this;
        vm.accountsIds = $routeParams.accountIds.split(",").filter(function (e) {
            return e.length > 3;
        });
        vm.accountsIds = vm.accountsIds.map(parseFloat);

        vm.evaluating = false;
        vm.teste = 'a';
        vm.accounts = [];
        vm.matches = [];
        vm.getNextPage = getNextPage;
        vm.loadingMessage = '';
        vm.currentPage = 0;
        vm.totalPages = 10000;

        active();

        function active() {

            vm.accountsIds.forEach(function (accId) {
                Profile.get(accId).then(function (data) {
                    vm.accounts.push(data.data);
                });
            });
        }

        function getNextPage() {
            if (vm.currentPage == vm.totalPages) {
                vm.loadingMessage = 'All matches loaded';
                return;
            }

            if (vm.evaluating) return;

            vm.evaluating = true;
            DetailMatch.getMatchesByAccountsIds(vm.accountsIds, vm.currentPage + 1).then(function (data) {
                vm.currentPage = data.data.current;
                vm.totalPages = data.data.total;

                vm.matches = vm.matches.concat(data.data.results);
                vm.matches.forEach(function(m) {
                    m.radiant_team = m.radiant_team || [];
                    m.dire_team = m.dire_team || [];
                });

                vm.matches.forEach(function(m){
                    m.against = false;
                   if (m.radiant_team.length != 0 && m.dire_team.length != 0) {
                       m.against = true;
                   } else if ((m.radiant_team.length != 0 && m.is_radiant_win) ||
                              (m.dire_team.length != 0 && !m.is_radiant_win)){
                       m.match_won = true;
                   } else {
                       m.match_won = false;
                   }
                });
                vm.evaluating = false;
            });
        }
    }
})();