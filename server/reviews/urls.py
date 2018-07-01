from django.conf.urls import include
from django.conf.urls import url

from reviews.views import ReviewList

urlpatterns = [
    url(r'^reviews/', ReviewList.as_view(), name='reviews'),
]
