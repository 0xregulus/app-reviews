# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.utils import timezone

User = get_user_model()
MIN_RATING_VALUE = 1
MAX_RATING_VALUE = 5
STATS_LAPSES = [7, 30, 90]  # In days


class Review(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def stats(cls):
        '''
        Get the overall stats of the app review
        :return: total reviews, average rating and average for each rating
        :rtype: ReviewStats object
        '''

        class ReviewStats(object):

            def __init__(self, query, *args, **kwargs):
                setattr(self, 'total_reviews', query.count())
                setattr(self, 'avg_rating', query.aggregate(Avg('rating')).get('rating__avg') or 0)
                for r in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1):
                    setattr(
                        self,
                        'total_{}_rates'.format(r),
                        query.filter(rating=r).aggregate(Count('rating')).get('rating__count') or 0
                    )
                    setattr(
                        self,
                        'avg_{}_rates'.format(r),
                        query.filter(rating=r).aggregate(Avg('rating')).get('rating__avg') or 0
                    )

        stats = ReviewStats(Review.objects.all())
        for tl in STATS_LAPSES:
            delta = timezone.now() + timezone.timedelta(days=-tl)
            lapse_stats = ReviewStats(Review.objects.filter(date_created__gte=delta))
            lapse_query = Review.objects.filter(date_created__gte=delta)
            setattr(stats, 'stats_last_{}_days'.format(tl), lapse_stats)

        return stats
