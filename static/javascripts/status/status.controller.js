(function () {
    'use strict';

    angular
        .module('dotaparty.status.controllers')
        .controller('StatusController', StatusController);

    StatusController.$inject = ['$location', 'Status', 'Root'];

    function StatusController($location, Status, Root) {
        var vm = this;
        vm.searchTxt = '';
        vm.find = find;
        vm.statistics = null;
        Root.setTitle("Status - Dota Party");
        active();

        function active() {
            Status.get().then(function (data) {
                vm.statistics = data.data;
                console.log(vm.statistics);
            });
            vm.elements = [mock(1), mock(2), mock(3), mock(4)];
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