# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.http import HttpResponse

from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status

from reviews.models import Review
from reviews.serializers import ReviewSerializer
from reviews.utils import JsonConvert


class Reviews(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class AdminReviews(ViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    @list_route(methods=['GET'], url_path='list')
    def list_reviews(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['GET'], url_path='stats')
    def stats(self, request, *args, **kwargs):
        json_str = JsonConvert.to_json(Review.stats())
        return Response(JsonConvert.from_json(json_str), status=status.HTTP_200_OK)

    @list_route(methods=['GET'], url_path='csv')
    def csv(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ratings.csv"'

        writer = csv.writer(response)
        writer.writerow(['Rating', 'Comment', 'User', 'Date'])
        for r in self.queryset:
            writer.writerow([r.rating, r.comment, r.user.email, r.date_created])

        return response
