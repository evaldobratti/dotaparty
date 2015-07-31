(function () {
    'use strict';

    angular
        .module('dotaparty.home.controllers')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$location', 'Home'];

    function HomeController($location, Home) {
        var vm = this;
        vm.searchTxt = '';
        vm.find = find;

        active();

        function active() {

        }

        function find() {
            Home.find(vm.searchTxt).then(function (result) {
                if (result.data.type == 'Account') {
                    console.log('ok, is acc');
                    $location.path('/profiles/' + result.data.result.account_id);
                }

            });
        }
    }
})();