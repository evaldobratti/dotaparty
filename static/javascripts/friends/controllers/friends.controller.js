(function () {
    'use strict';

    angular
        .module('dotaparty.friends.controllers')
        .controller('FriendsController', FriendsController);

    FriendsController.$inject = ['$routeParams', 'Friends', 'Profile'];

    function FriendsController($routeParams, Friends, Profile) {
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
                Profile.getAccount(accId).then(function (data) {
                    vm.accounts.push(data.data);
                });
            });

        /*Friends.get(vm.accountsIds).then(function (data) {
                vm.matches = data.data;
                filterPlayers(vm.matches.results);

                vm.currentPage = data.data.current;
                vm.totalPages = data.data.total;
            })*/

        }

        function getNextPage() {
            if (vm.currentPage == vm.totalPages) {
                vm.loadingMessage = 'All matches loaded';
                return;
            }

            if (vm.evaluating) return;

            vm.evaluating = true;
            Friends.getPage(vm.accountsIds, vm.currentPage + 1).then(function (data) {
                vm.currentPage = data.data.current;
                vm.totalPages = data.data.total;
                filterPlayers(data.data.results);

                vm.matches = vm.matches.concat(data.data.results);
                vm.evaluating = false;
            });
        }

        function filterPlayers(matches) {
            matches.forEach(function (match) {
                match.playersFiltered = [];
                match.radiant_team.forEach(function (player) {
                    if (vm.accountsIds.indexOf(player.account_id) >= 0) {
                        match.playersFiltered.push(player);
                        match.wereOnRadiant = true;
                    }
                });
                match.dire_team.forEach(function (player) {
                    if (vm.accountsIds.indexOf(player.account_id) >= 0) {
                        match.playersFiltered.push(player);
                        match.wereOnRadiant = false;
                    }
                });

            });
        }
    }
})();