# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
