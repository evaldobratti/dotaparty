(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('DetailMatchController', DetailMatchController);

    DetailMatchController.$inject = ['$routeParams', 'DetailMatch', 'Profile'];

    function DetailMatchController($routeParams, DetailMatch, Profile) {
        var vm = this;
        vm.friendsMatches = friendsMatches;
        vm.matches_with = [];
        vm.current_selected = null;

        active();

        function active() {
            var matchId = $routeParams.matchId;
            DetailMatch.get(matchId).then(function (result) {
                vm.match = result.data;
                vm.match.players = vm.match.radiant_team.concat(vm.match.dire_team);

                vm.labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25];
                vm.data = [];
                vm.series = [];
                vm.match.players.forEach(function (player) {
                    var upgradesTime = [];
                    player.abilities.reverse().forEach(function (upgrade) {
                        upgradesTime.push(upgrade.time);
                    });
                    vm.data.push(upgradesTime);
                    vm.series.push(player.hero.localized_name);
                });

            });
        }

        function friendsMatches(player) {
            if (player.player_account == null)
                return;
            vm.current_selected = player;
            Profile.getPlayersMatches(player.account_id, othersRealPlayers(player)).then(function (result) {
                vm.matches_with.push(result.data);

                vm.match.players.forEach(function(player) {
                    player.matches_with = null;
                    result.data.friends.forEach(function(friend) {
                       if (player.account_id == friend.account_id) {
                           player.matches_with = friend.qtd;
                       }
                    });
                });

            });
        }

        function othersRealPlayers(subject) {
            var others_ids = [];
            vm.match.players.forEach(function (p) {
                if (p.player_account != null && subject != p)
                    others_ids.push(p.account_id);
            });
            return others_ids;
        }

    }
})();