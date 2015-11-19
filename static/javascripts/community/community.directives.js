(function () {
    'use strict';

    angular
        .module('dotaparty.community.directives')
        .directive('report', report);

    function report() {
        var directive = {
            restrict: 'E',
            scope: {
                report: '=',
                mode: '='
            },
            templateUrl: '/static/templates/community/report.html'
        };

        return directive;
    }
})();