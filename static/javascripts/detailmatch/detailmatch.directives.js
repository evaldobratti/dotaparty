(function () {
    'use strict';

    angular
        .module('dotaparty.detailmatch.directives')
        .directive('detailmatchteam', detailmatchteam);

    function detailmatchteam() {
        var directive = {
            restrict: 'E',
            scope: {
                team: '=',
                vm: '=controller'
            },
            templateUrl: '/static/templates/detailmatch/team.html'
        };

        return directive;
    }
})();