(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('DetailMatchController', DetailMatchController);

    DetailMatchController.$inject = ['$scope', '$routeParams', 'DetailMatch']

    function DetailMatchController($scope, $routeParams, DetailMatch) {
        var vm = this;

        active();

        function active() {
            var matchId = $routeParams.matchId;
            DetailMatch.get(matchId).then(function(result) {
                console.log(result.data);
                vm.match = result.data;
            });
        }
    }
})();