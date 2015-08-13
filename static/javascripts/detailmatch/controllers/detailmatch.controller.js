(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('DetailMatchController', DetailMatchController);

    DetailMatchController.$inject = ['$routeParams', 'DetailMatch'];

    function DetailMatchController($routeParams, DetailMatch) {
        var vm = this;


        active();

        function active() {
            var matchId = $routeParams.matchId;
            DetailMatch.get(matchId).then(function (result) {
                vm.match = result.data;

                vm.labels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];
                vm.data = [];
                vm.series = [];
                vm.match.dire_team.forEach(function(player) {
                    var upgradesTime = [];
                    player.abilities.reverse().forEach(function(upgrade) {
                        upgradesTime.push(upgrade.time);
                    })
                    vm.data.push(upgradesTime);
                    vm.series.push(player.hero.localized_name);
                });
                vm.match.radiant_team.forEach(function(player) {
                    var upgradesTime = [];
                    player.abilities.reverse().forEach(function(upgrade) {
                        upgradesTime.push(upgrade.time);
                    })
                    vm.data.push(upgradesTime);
                    vm.series.push(player.hero.localized_name);
                });

            });
        }
    }
})();