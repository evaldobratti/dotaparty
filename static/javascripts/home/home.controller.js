(function () {
    'use strict';

    angular
        .module('dotaparty.home.controllers')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$location', 'Home', '$rootScope', 'Root'];

    function HomeController($location, Home, $rootScope, Root) {
        var vm = this;
        vm.searchTxt = $location.search().q;
        vm.find = find;
        $rootScope.query = vm.searchTxt ;
        vm.buscaFeita = false;
        vm.setSearch = setSearch;
        Root.setTitle('Dota Party');

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
                }
                vm.buscaFeita = true;
            });
        }

        function setSearch() {
            $location.path('/');
            $location.search({
                q: $rootScope.query
            });
        }
    }
})();