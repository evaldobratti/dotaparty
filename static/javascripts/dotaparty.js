(function () {
    'use strict';

    angular
        .module('dotaparty', [
            'dotaparty.routes',
            'dotaparty.config',
            'dotaparty.detailmatch'
        ]);

    angular.module('dotaparty.routes', ['ngRoute']);
    angular.module('dotaparty.config', [])
})();