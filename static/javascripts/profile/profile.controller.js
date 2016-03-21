(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$rootScope', '$routeParams', 'Profile', 'DetailMatch', 'Root'];

    function ProfileController($rootScope, $routeParams, Profile, DetailMatch, Root) {
        var vm = this;
        vm.accountId = $routeParams.accountId;

        vm.currentDetailMatchesPage = Root.search().matchPage == undefined ? 1 : Root.search().matchPage;
        vm.totalMatchesPages = -1;
        vm.downloadGames = downloadGames;
        vm.loadMatchesPage = loadMatchesPage;
        vm.matches = null;
        vm.account = null;
        vm.friends = null;
        vm.reportsReceived = [];
        vm.reportsCreated = [];
        vm.matchesCache = {};
        vm.availableToDownload = null;
        vm.availableToDownloadMessage = null;

        vm.matchesPaginationIndexes = [1, 2, 3];

        active();

        function active() {
            Profile.get(vm.accountId).then(function (result) {
                vm.account = result.data;
                Root.setTitle(vm.account.current_update.persona_name + ' - Profile - Dota Party')
            });

            Profile.getFriends(vm.accountId).then(function (result){
               vm.friends = result.data.friends;
            });

            Profile.getReportsCreated(vm.accountId).then(function (result){
               vm.reportsCreated = result.data;
            });

            Profile.getReportsReceived(vm.accountId).then(function (result){
               vm.reportsReceived = result.data;
            });

            Profile.isAvailableToDownload(vm.accountId).then(function(result) {
                vm.availableToDownload = true
            }, function (error) {
                vm.availableToDownload = false;
                vm.availableToDownloadMessage = error.data.error;
            });
            loadMatchesPage(vm.currentDetailMatchesPage);
            
        }

        function loadMatchesPage(page) {
            if (vm.matchesCache['m' + page] != undefined) {
                 loadMatches(vm.matchesCache['m' + page], page, vm.totalMatchesPages);
            } else {   
                DetailMatch.getMatchesByAccountsIds(vm.accountId, page).then(function (data) {
                    loadMatches(data.data.results, page, data.data.total);
                    determineVictoryOrLoss(vm.matches);
                });
            }
        }

        function loadMatches(matches, page, totalPages)  {
            vm.matches = matches;
            vm.currentDetailMatchesPage = page;
            vm.matchesCache['m' + page] = matches;
 
            if (page == 1){
                Root.setLocation({search:{}});
            } else {
                Root.setLocation({search:{'matchPage': page}});
            }


            updatePages(totalPages);
            determineVictoryOrLoss(vm.matches);
        }

        function updatePages(pagesTotal) {
            var bottomLimit = Math.max(1, vm.currentDetailMatchesPage - 2);
            var topLimit = Math.min(pagesTotal, vm.currentDetailMatchesPage + 2);
            vm.totalMatchesPages = pagesTotal;
    
            vm.matchesPaginationIndexes = [];
            for (var i=bottomLimit; i <= topLimit; i++) {
                vm.matchesPaginationIndexes.push(i);
            }
            
        }

        function downloadGames() {
            Profile.downloadGames(vm.account.account_id).
                success(function () {
                    vm.account.matches_download_required = true;
                }).
                error(function () {
                    $rootScope.alerts.push({
                        type: 'danger',
                        msg: 'It was not possible to download your games due to an internal error.'
                    });
                });

        }

        function determineVictoryOrLoss(matches) {
            matches.forEach(function (match) {
                if (match.is_radiant_win)
                    match.match_won = match.radiant_team.length > 0;
                else
                    match.match_won = match.dire_team.length > 0;

            });
        }
    }
})();