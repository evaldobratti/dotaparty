(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('DetailMatchController', DetailMatchController);

    DetailMatchController.$inject = ['$routeParams', 'DetailMatch'];

    function DetailMatchController($routeParams, DetailMatch) {
        var vm = this;
        vm.IMG_WIDTH = 30;
        active();

        function active() {
            var matchId = $routeParams.matchId;
            DetailMatch.get(matchId).then(function(result) {
                vm.match = result.data;
            })
        }
    }
})();