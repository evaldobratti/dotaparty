(function () {
    'use strict';

    angular
        .module('dotaparty.friends.controllers')
        .controller('FriendsController', FriendsController);

    FriendsController.$inject = ['$routeParams', 'Friends'];

    function FriendsController($routeParams, Friends) {
        var vm = this;
        vm.teste = 'a';

        active();

        function active() {


        }
    }
})();