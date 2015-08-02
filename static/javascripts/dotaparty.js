(function () {
    'use strict';

    angular
        .module('dotaparty', [
            'infinite-scroll',
            'dotaparty.routes',
            'dotaparty.config',
            'dotaparty.detailmatch',
            'dotaparty.profile',
            'dotaparty.friends',
            'dotaparty.home'
        ]);

    angular.module('dotaparty.routes', ['ngRoute']);
    angular.module('dotaparty.config', [])
})();