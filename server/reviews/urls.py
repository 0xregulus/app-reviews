from django.conf.urls import include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from reviews.views import Reviews, AdminReviews


admin_router = DefaultRouter()
admin_router.register(r'admin-reviews', AdminReviews, base_name='admin-reviews')

urlpatterns = [
    url(r'^reviews/', Reviews.as_view(), name='reviews'),
    url(r'^', include(admin_router.urls)),
]
