'use strict';

var myServices = angular.module('reviewServices', ['ngResource']);

myServices.factory('Authy', ['$resource',
    function($resource) {
        return $resource('http://localhost:8000/authy/', {}, {
            login: {
                method: 'POST'
            }
        });
    }
]);

myServices.factory('Review', ['$resource',
    function($resource) {
        return $resource('http://localhost:8000/reviews/', {}, {
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

myServices.factory('Admin', ['$resource',
    function($resource) {
        return $resource('http://localhost:8000/admin-reviews/', {}, {
            list: {
                method: 'GET',
                isArray: true,
                url: 'http://localhost:8000/admin-reviews/list/'
            },
            stats: {
                method: 'GET',
                url: 'http://localhost:8000/admin-reviews/stats/'
            },
            csv: {
                method: 'GET',
                url: 'http://localhost:8000/admin-reviews/csv/'
            }
        });
    }
]);
