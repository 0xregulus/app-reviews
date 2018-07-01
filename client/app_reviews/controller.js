angular.module('appReviews', ['ngMaterial', 'angularRatingStars', 'reviewServices'])

.controller('reviewCtrl', function($scope, Review) {
    $scope.firstRate = 0;
    $scope.onRating = function(rating, comment){
        if (!comment) {
            alert("Don't you wanna leave a comment?")
        } else {
            console.log(rating, comment);
            alert('Thanks for your opinion!');
        }
    };
});
