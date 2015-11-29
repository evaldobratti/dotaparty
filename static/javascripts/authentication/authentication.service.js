(function () {
    'use strict';

    angular
        .module('dotaparty.authentication.services')
        .service('Authentication', Authentication);

    Authentication.$inject = ['$http', '$q'];

    function Authentication($http, $q) {
        var vm = this;
        vm.authenticated = null;

        var Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated
        };

        active();
        function active() {
            if (vm.authenticated == null) {

                var xhr = new XMLHttpRequest();
                xhr.open("GET", "api/user/", false);
                xhr.onload = function(e) {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            vm.authenticated = JSON.parse(xhr.responseText);
                        }
                    }
                };
                xhr.onerror = function (e) {
                  vm.authenticated = { 'is_authenticated': false }
                };
                xhr.send(null);


            }
        }
        return Authentication;

        function getAuthenticatedAccount() {
            if (vm.authenticated.is_authenticated)
                return vm.authenticated;
            return null;
        }

        function isAuthenticated() {
            return vm.authenticated != null && vm.authenticated.is_authenticated;
        }
    }
})();