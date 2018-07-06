'use strict';

var myControllers = angular.module('reviewsControllers', ['reviewServices', 'ngMaterial', 'angularRatingStars', 'googlechart']);

myControllers.controller('loginCtrl', function($rootScope, $scope, Authy) {
    $rootScope.user = null;
    $scope.login = function(username, password){
        Authy.login(
            {
                'username': username,
                'password': password
            },
            function(response) {
                $rootScope.user = response;
                document.getElementById("login-holder").style.display = "none";
                if ($rootScope.user.is_staff){
                    document.getElementById("admin").style.display = "block";
                } else {
                    document.getElementById("main").style.display = "block";
                }
            },
            function(error) {
                console.log(error);
                alert('Oops! Somothing went wrong.');
            }
        );
    };
});

myControllers.controller('reviewCtrl', function($rootScope, $scope, Review) {
    $scope.firstRate = 0;
    $scope.onRating = function(rating, comment){
        if (!comment) {
            alert("Don't you wanna leave a comment?")
        } else {
            Review.post(
                {
                    'user': $rootScope.user.id,
                    'rating': rating,
                    'comment': comment
                },
                function(response) {
                    alert('Thanks for your opinion!');
                },
                function(error) {
                    console.log(error);
                    alert('Oops! Somothing went wrong.');
                }
            );
        }
    };
});

myControllers.controller('adminCtrl', function($scope, $window, Admin) {
    $scope.reviewChart = {type: "BarChart", options: {title: "Lifetime totals"}};
    $scope.review7Chart = {type: "BarChart", options: {title: "Last week totals"}};
    $scope.review30Chart = {type: "BarChart", options: {title: "Last 30 days totals"}};
    $scope.review90Chart = {type: "BarChart", options: {title: "Last 90 days totals"}};
    Admin.stats(
        {},
        function(response) {
            $scope.stats = response;
            $scope.reviewChart.data = {
                "cols": [
                    {id: "s", label: "Stars", type: "string"},
                    {id: "t", label: "Total rates", type: "number"}
                ], "rows": [
                    {c: [
                        {v: "1 Star"},
                        {v: $scope.stats.total_1_rates},
                    ]},
                    {c: [
                        {v: "2 Stars"},
                        {v: $scope.stats.total_2_rates},
                    ]},
                    {c: [
                        {v: "3 Stars"},
                        {v: $scope.stats.total_3_rates},
                    ]},
                    {c: [
                        {v: "4 Stars"},
                        {v: $scope.stats.total_4_rates},
                    ]},
                    {c: [
                        {v: "5 Stars"},
                        {v: $scope.stats.total_5_rates},
                    ]}
                ]
            };
            $scope.review7Chart.data = {
                "cols": [
                    {id: "s", label: "Stars", type: "string"},
                    {id: "t", label: "Total rates", type: "number"}
                ], "rows": [
                    {c: [
                        {v: "1 Star"},
                        {v: $scope.stats.stats_last_7_days.total_1_rates},
                    ]},
                    {c: [
                        {v: "2 Stars"},
                        {v: $scope.stats.stats_last_7_days.total_2_rates},
                    ]},
                    {c: [
                        {v: "3 Stars"},
                        {v: $scope.stats.stats_last_7_days.total_3_rates},
                    ]},
                    {c: [
                        {v: "4 Stars"},
                        {v: $scope.stats.stats_last_7_days.total_4_rates},
                    ]},
                    {c: [
                        {v: "5 Stars"},
                        {v: $scope.stats.stats_last_7_days.total_5_rates},
                    ]}
                ]
            };
            $scope.review30Chart.data = {
                "cols": [
                    {id: "s", label: "Stars", type: "string"},
                    {id: "t", label: "Total rates", type: "number"}
                ], "rows": [
                    {c: [
                        {v: "1 Star"},
                        {v: $scope.stats.stats_last_30_days.total_1_rates},
                    ]},
                    {c: [
                        {v: "2 Stars"},
                        {v: $scope.stats.stats_last_30_days.total_2_rates},
                    ]},
                    {c: [
                        {v: "3 Stars"},
                        {v: $scope.stats.stats_last_30_days.total_3_rates},
                    ]},
                    {c: [
                        {v: "4 Stars"},
                        {v: $scope.stats.stats_last_30_days.total_4_rates},
                    ]},
                    {c: [
                        {v: "5 Stars"},
                        {v: $scope.stats.stats_last_30_days.total_5_rates},
                    ]}
                ]
            };
            $scope.review90Chart.data = {
                "cols": [
                    {id: "s", label: "Stars", type: "string"},
                    {id: "t", label: "Total rates", type: "number"}
                ], "rows": [
                    {c: [
                        {v: "1 Star"},
                        {v: $scope.stats.stats_last_90_days.total_1_rates},
                    ]},
                    {c: [
                        {v: "2 Stars"},
                        {v: $scope.stats.stats_last_90_days.total_2_rates},
                    ]},
                    {c: [
                        {v: "3 Stars"},
                        {v: $scope.stats.stats_last_90_days.total_3_rates},
                    ]},
                    {c: [
                        {v: "4 Stars"},
                        {v: $scope.stats.stats_last_90_days.total_4_rates},
                    ]},
                    {c: [
                        {v: "5 Stars"},
                        {v: $scope.stats.stats_last_90_days.total_5_rates},
                    ]}
                ]
            };
        },
        function(error) {
            console.log(error);
            alert('Oops! Somothing went wrong.');
        }
    );

    Admin.list(
        {},
        function(response) {
            $scope.reviews = response;
        },
        function(error) {
            console.log(error);
            alert('Oops! Somothing went wrong.');
        }
    );

    $scope.csv = function() {
        $window.open('http://localhost:8000/admin-reviews/csv/', '_blank');
    };

});
