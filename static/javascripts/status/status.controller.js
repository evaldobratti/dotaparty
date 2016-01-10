(function () {
    'use strict';

    angular
        .module('dotaparty.status.controllers')
        .controller('StatusController', StatusController);

    StatusController.$inject = ['$location', 'Home'];

    function StatusController($location, Home) {
        var vm = this;
        vm.searchTxt = '';
        vm.find = find;

        active();

        function active() {
            vm.elements = [mock(1),mock(2),mock(3),mock(4)];
        }

        function mock(index) {
            return {
                match_id: index + 123123123,
                players: [{
                    persona_name: "Some 1 " + index,
                    account_id: index + 34344
                }, {
                    persona_name: "Some 2 " + index,
                    account_id: index + 34344
                }]
            }
        }
    }
})();