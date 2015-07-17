(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$scope', '$routeParams', 'Profile']

    function ProfileController($scope, $routeParams, Profile) {
        var vm = this;

        active();

        function active() {
            var accountId = $routeParams.accountId;
            Profile.get(accountId).then(function(result) {
                vm.account = result.data;
            });
        }
    }
})();