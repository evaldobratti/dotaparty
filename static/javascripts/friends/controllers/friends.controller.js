(function () {
    'use strict';

    angular
        .module('dotaparty.friends.controllers')
        .controller('FriendsController', FriendsController);

    FriendsController.$inject = ['$routeParams', 'Friends', 'Profile'];

    function FriendsController($routeParams, Friends, Profile) {
        var vm = this;
        vm.teste = 'a';
        vm.accounts = [];

        active();

        function active() {
            var accountsIds = $routeParams.accountIds.split("/").filter(function(e) {return e.length > 3; });;
            accountsIds.forEach(function (accId) {
               Profile.getAccount(accId).then(function(data) {
                   vm.accounts.push(data.data);
               });
            });
        }
    }
})();