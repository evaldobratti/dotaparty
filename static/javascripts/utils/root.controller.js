(function () {
    'use strict';

    angular
        .module('dotaparty.utils.services')
        .service('Root', Root);

    Root.$inject = ['$rootScope', '$location'];

    function Root($rootScope, $location) {
        $rootScope.title = 'Dota Party';

        var Root = {
            setTitle: setTitle,
            setLocation: setLocation,
            search: search,
            redirect404: redirect404
        };

        return Root;

        function redirect404() {
            setTitle("Not found :( - Dota Party");
            setLocation({
                path: "/404"
            });
        }

        function setTitle(title) {
            $rootScope.title = title;
        }

        function setLocation(pathAndSearch) {
            if (pathAndSearch.path != undefined)
                $location.path(pathAndSearch.path);

            if (pathAndSearch.search != undefined)
                $location.search(pathAndSearch.search);
        }

        function search() {
            return $location.search();
        }
    }
})();
