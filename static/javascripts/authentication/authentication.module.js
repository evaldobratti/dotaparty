(function () {
    'use strict';

    angular
        .module('dotaparty.authentication', [
            'dotaparty.authentication.services'
        ]);

    angular
        .module('dotaparty.authentication.services', [ 'ngCookies' ]);
})();