! function() {
    "use strict";
    angular.module("angularRatingStars", ["angularRatingStars.templates"])
}(),
function() {
    "use strict";

    function RatingStarsController($scope, $attrs, $timeout) {
        var that = this;
        that.initStarsArray = function() {
            that.starsArray = that.getStarsArray(), that.validateStars()
        }, that.getStarsArray = function() {
            for (var starsArray = [], index = 0; index < that.maxRating; index++) {
                var starItem = {
                    index: index,
                    "class": "star-off"
                };
                starsArray.push(starItem)
            }
            return starsArray
        }, that.setRating = function(rating, comment) {
            that.rating = rating, that.validateStars(that.rating)
        }, that.postRating = function(rating, comment) {
            that.onRating({
                rating: rating,
                comment: comment
            }), $scope.$apply()
        }, that.setMouseOverRating = function(rating) {
            that.validateStars(rating)
        }, that.validateStars = function(rating) {
            if (that.starsArray && 0 !== that.starsArray.length)
                for (var index = 0; index < that.starsArray.length; index++) {
                    var starItem = that.starsArray[index];
                    rating - 1 >= index ? starItem["class"] = "star-on" : starItem["class"] = "star-off"
                }
        }
    }
    angular.module("angularRatingStars").controller("RatingStarsController", ["$scope", "$attrs", "$timeout", RatingStarsController])
}(),
function() {
    "use strict";

    function RatingStarsDirective() {
        function link(scope, element, attrs, ctrl) {
            (!attrs.maxRating || parseInt(attrs.maxRating) <= 0) && (attrs.maxRating = "5"), scope.$watch("ctrl.maxRating", function(oldVal, newVal) {
                ctrl.initStarsArray()
            }), scope.$watch("ctrl.rating", function(oldVal, newVal) {
                ctrl.validateStars(ctrl.rating)
            })
        }
        return {
            restrict: "E",
            replace: !0,
            templateUrl: "rating-stars-directive.html",
            scope: {},
            controller: "RatingStarsController",
            controllerAs: "ctrl",
            bindToController: {
                maxRating: "@?",
                rating: "=?",
                onRating: "&"
            },
            link: link
        }
    }
    angular.module("angularRatingStars").directive("ratingStars", [RatingStarsDirective])
}(),
function() {
    angular.module("angularRatingStars.templates", []).run(["$templateCache", function($templateCache) {
        $templateCache.put("rating-stars-directive.html", '<div class="rating-container" layout="column"><div class="rating-stars-container" layout="row"><a class="button star-button" ng-class="item.class" ng-mouseover="ctrl.setMouseOverRating($index + 1)" ng-mouseleave="ctrl.setMouseOverRating(ctrl.rating)" ng-click="ctrl.setRating($index + 1)" ng-repeat="item in ctrl.starsArray" ><i class="material-icons">star</i></div><div class="rating-comment-container" layout="row"></a><textarea ng-model="ctrl.comment" rows="4" cols="40"></textarea><md-button class="md-raised md-primary" ng-click="ctrl.postRating(ctrl.rating, ctrl.comment)">Rate!</md-button></div>')
    }])
}();
