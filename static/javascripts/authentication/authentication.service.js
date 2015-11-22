(function () {
    'use strict';

    angular
        .module('dotaparty.authentication.services')
        .service('Authentication', Authentication);

    Authentication.$inject = ['$http'];

    function Authentication($http) {
        this.authenticated = undefined;

        var Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount
        };

        return Authentication;

        function getAuthenticatedAccount() {
            if (this.authenticated == undefined) {
                console.log('nao tenho informação, vou pegar no servidor');
                this.authenticated = 'hoho haha';
            }

            console.log('tenho informação, retorno');
            return this.authenticated;
        }
    }
})();