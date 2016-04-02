(function () {
    'use strict';


    angular
        .module('dotaparty', [
            'infinite-scroll',
            'ui.bootstrap',
            'angular-loading-bar',
            'dotaparty.routes',
            'dotaparty.config',
            'dotaparty.detailmatch',
            'dotaparty.profile',
            'dotaparty.friends',
            'dotaparty.home',
            'dotaparty.filter',
            'dotaparty.alerts',
            'dotaparty.community',
            'dotaparty.authentication',
            'dotaparty.utils',
            'dotaparty.status',
            'ngDialog'
        ]);

    angular.module('dotaparty.routes', ['ui.router']);
    angular.module('dotaparty.config', []);
    angular.module('dotaparty.filter', []);

    angular.module('dotaparty.alerts', []).controller('AlertsController', function ($rootScope) {
        $rootScope.alerts = [ ];

        $rootScope.closeAlert = function (index) {
            $rootScope.alerts.splice(index, 1);
        };
    });
})();


$(document).arrive('[data-toggle="tooltip"]', function() {
    $(this).tooltip();
});

$.material.init();
