(function () {
    'use strict';

    angular
        .module('dotaparty.utils.bootstrap')
        .factory('Bootstrap', Bootstrap);

    Bootstrap.$inject = [];

    function Bootstrap() {
        var Bootstrap = {
            init: init
        };

        return Bootstrap;

        function init() {
            $.material.init();
            $('[data-toggle="tooltip"]').tooltip();
        }
    }
})();