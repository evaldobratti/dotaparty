(function () {
    'use strict';

    var module = angular.module('dotaparty.filter');
    module.filter('secondsToDateTime', [function () {
            return function (seconds) {
                return new Date(1970, 0, 1).setSeconds(seconds);
            };
        }]);

    module.filter('abbreviate', [function() {
        return function(number) {
            if (number < 1000)
                return number.toString();

            var milhares = Math.floor(number / 1000);
            var centenas = number % 1000;

            return milhares.toString() + '.' + centenas.toString()[0] + 'k  ';

        }
    }])
})();