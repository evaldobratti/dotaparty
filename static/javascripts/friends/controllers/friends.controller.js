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


        vm.teste = 'a';
        vm.accounts = [];
        vm.matches = [];
        vm.getNextPage = getNextPage;

        active();

        function active() {

            vm.accountsIds.forEach(function (accId) {
                Profile.getAccount(accId).then(function (data) {
                    vm.accounts.push(data.data);
                });
            });

            Friends.get(vm.accountsIds).then(function (data) {
                vm.matches = data.data;
                filterPlayers(vm.matches.results);

                vm.currentPage = data.data.current;
                vm.totalPages = data.data.total;
            })

        }

        function getNextPage() {
            Friends.getPage(vm.accountsIds, vm.currentPage + 1).then(function (data) {
                vm.currentPage = data.data.current;
                filterPlayers(data.data.results);
                vm.matches.results = vm.matches.results.concat(data.data.results);
            });
        }

        function filterPlayers(matches) {
            matches.forEach(function (match) {
                match.playersFiltered = [];
                match.players.forEach(function (player) {
                    console.log(vm.accountsIds);
                    if (vm.accountsIds.indexOf(player.account_id) >= 0) {

                        match.playersFiltered.push(player);
                    }

                });

            });
        }
    }
})();