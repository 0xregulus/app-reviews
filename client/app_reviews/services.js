angular.module('reviewServices', ['ngResource'])

.factory('Review', ['$resource',
    function($resource) {
        return $resource('/reviews/', {}, {
            get: {
                method: 'GET',
                isArray: true
            },
            post: {
                method: 'POST'
            }
        });
    }
]);
