(function () {
    'use strict';

    angular
        .module('dotaparty.authentication.services')
        .service('Authentication', Authentication);

    Authentication.$inject = ['$http'];

    function Authentication($http) {
        var vm = this;
        vm.authenticated = undefined;
        vm.locked = false;

        var Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount
        };

        return Authentication;

        function getAuthenticatedAccount() {
            if (vm.authenticated == undefined) {
                vm.locked = true;
                $http.get('api/user/').then(function(data) {
                    vm.authenticated = data.data;
                    vm.locked = false;
                });
            }
            while(vm.locked) {}
            console.log(vm.authenticated);
            return vm.authenticated;
        }
    }
})();