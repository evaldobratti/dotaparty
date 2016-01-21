(function () {
    'use strict';

    angular
        .module('dotaparty.home.controllers')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$location', 'Home', '$rootScope'];

    function HomeController($location, Home, $rootScope) {
        var vm = this;
        vm.searchTxt = $location.search().q;
        vm.find = find;
        $rootScope.query = vm.searchTxt ;
        vm.buscaFeita = false;

        active();

        function active() {
            if (vm.searchTxt)
                find();
        }

        function find() {
            Home.find(vm.searchTxt).then(function (result) {
                vm.accounts = result.data.accounts;
                vm.matches = result.data.matches;

                if (vm.matches.length == 1) {
                    $location.path('/matches/' + vm.matches[0].match_id, {});
                    $location.search({});
                    $location.replace();
                }
                vm.buscaFeita = true;
            });
        }
    }
})();