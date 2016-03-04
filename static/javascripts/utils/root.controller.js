(function () {
    'use strict';

    angular
        .module('dotaparty.utils.services')
        .service('Root', Root);

    Root.$inject = ['$rootScope'];

    function Root($rootScope) {
        $rootScope.title = 'Dota Party';

        var Root = {
            setTitle: setTitle
        };

        return Root;

        function setTitle(title) {
            $rootScope.title = title;
        }
    }
})();
