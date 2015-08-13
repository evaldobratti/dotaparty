(function () {
    'use strict';


    angular
        .module('dotaparty', [
            'infinite-scroll',
            'ui.bootstrap',
            'dotaparty.routes',
            'dotaparty.config',
            'dotaparty.detailmatch',
            'dotaparty.profile',
            'dotaparty.friends',
            'dotaparty.home',
            'dotaparty.filter',
            'dotaparty.alerts'
        ]);

    angular.module('dotaparty.routes', ['ngRoute']);
    angular.module('dotaparty.config', []);
    angular.module('dotaparty.filter', []);

    angular.module('dotaparty.alerts', []).controller('AlertsController', function ($rootScope) {
        $rootScope.alerts = [ ];

        $rootScope.closeAlert = function (index) {
            $rootScope.alerts.splice(index, 1);
        };
    });
})();