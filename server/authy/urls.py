from django.conf.urls import include
from django.conf.urls import url

from authy.views import AuthView

urlpatterns = [
    url(r'^authy/', AuthView.as_view(), name='authy'),
]
