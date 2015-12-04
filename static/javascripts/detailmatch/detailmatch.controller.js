(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('DetailMatchController', DetailMatchController);

    DetailMatchController.$inject = ['$routeParams', 'DetailMatch', 'Profile', 'ngDialog', 'Authentication'];

    function DetailMatchController($routeParams, DetailMatch, Profile, ngDialog, Authentication) {
        var vm = this;
        vm.friendsMatches = friendsMatches;
        vm.report = report;
        vm.matches_with = [];
        vm.current_selected = null;
        vm.played_with = {};
        vm.authenticated = false;
        vm.authenticatedAccount = null;
        vm.enableReportPlayer = enableReportPlayer;

        active();

        function active() {
            var matchId = $routeParams.matchId;
            vm.authenticatedAccount = Authentication.getAuthenticatedAccount();
            vm.isAuthenticated = Authentication.isAuthenticated();
            DetailMatch.get(matchId).then(function (result) {
                vm.match = result.data;
                vm.match.players = vm.match.radiant_team.concat(vm.match.dire_team);
            });

        }

        function friendsMatches(player) {


            if (player.player_account == undefined)
                return;
            if (vm.played_with[player.player_account.account_id.toString()] != undefined) {
                loadPlayedWithForPlayerFrom(player, vm.played_with[player.player_account.account_id.toString()]);
            } else {
                Profile.getPlayersMatches(player.player_account.account_id, othersRealPlayers(player)).then(function (result) {
                    loadPlayedWithForPlayerFrom(player, result.data);
                });
            }

        }

        function loadPlayedWithForPlayerFrom(player, matches_with) {
            vm.current_selected = player;
            vm.played_with[player.player_account.account_id.toString()] = matches_with;

            vm.match.players.forEach(function(player) {
                    player.matches_with = null;
                    matches_with.friends.forEach(function(friend) {
                       if (player.player_account != undefined && player.player_account.account_id == friend.account_id) {
                           player.matches_with = friend.qtd;
                       }
                    });
                });
        }

        function othersRealPlayers(currentPlayer) {
            var others_ids = [];
            vm.match.players.forEach(function (p) {
                if (p.player_account != null && currentPlayer != p)
                    others_ids.push(p.player_account.account_id);
            });
            return others_ids;
        }

        function report(player) {
            ngDialog.open({
                template: "/static/templates/community/new-report.html",
                controller: "NewReportController as vm",
                resolve: {
                    reportedPlayer: function() { return player; },
                    matchId: function() { return vm.match.match_id; }
                }
            });
        }

        function enableReportPlayer(p) {
            return vm.isAuthenticated && p.player_account != null && p.player_account.account_id != vm.authenticatedAccount.account_id;
        }


    }
})();