'use strict';

var app = angular.module('appReviews', ['reviewServices', 'reviewsControllers']);

app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.run(function($rootScope, $location) {
    if ($rootScope.user) {
        if ($rootScope.user.is_staff){
            document.getElementById("admin").style.display = "block";
        } else {
            document.getElementById("main").style.display = "block";
        }
    } else {
        document.getElementById("login-holder").style.display = "block";
    }
});
