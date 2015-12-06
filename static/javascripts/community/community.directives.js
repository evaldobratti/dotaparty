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
            templateUrl: '/static/templates/community/report.html',
            controller: ['$scope', function($scope) {
                    $scope.showHeader = function(report) {
                        if ($scope.mode == 'created' && report.creator != null)
                            return true;

                        if ($scope.mode == 'received' && report.reported != null)
                            return true;

                        return false;
                    }
                }]

        };

        return directive;
    }
})();