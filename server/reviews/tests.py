# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from reviews.models import Review, MIN_RATING_VALUE, MAX_RATING_VALUE, STATS_LAPSES

User = get_user_model()


class TestReview(TestCase):

    def test_create_review(self):
        user = User.objects.create_user(
            'testuser', 'user@test.com', 'insertstrongpassword'
        )
        review = Review.objects.create(user=user, rating=5, comment='what a great app!')
        self.assertFalse(review.id is None)
        self.assertEqual(review.user, user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'what a great app!')

    def test_review_stats(self):
        stats = Review.stats()
        self.assertEqual(stats.total_reviews, 0)
        self.assertEqual(stats.avg_rating, 0)
        for r in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1):
            self.assertEqual(getattr(stats, 'total_{}_rates'.format(r)), 0)
            self.assertEqual(getattr(stats, 'avg_{}_rates'.format(r)), 0)

        for r in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1):
            user = User.objects.create_user(
            'testuser{}'.format(r), 'user{}@test.com'.format(r), 'insertstrongpassword'
            )
            Review.objects.create(user=user, rating=r, comment='Comment {}'.format(r))

        stats = Review.stats()
        self.assertEqual(stats.total_reviews, MAX_RATING_VALUE)
        self.assertEqual(
            stats.avg_rating,
            sum([i for i in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1)]) / MAX_RATING_VALUE
        )
        for r in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1):
            self.assertEqual(getattr(stats, 'total_{}_rates'.format(r)), 1)
            self.assertEqual(getattr(stats, 'avg_{}_rates'.format(r)), r)


class TestReviewAPI(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'insertstrongpassword'
        self.user = User.objects.create_user(
            self.username, 'user@test.com', self.password
        )
        self.client = APIClient()

    def test_no_data(self):
        url = reverse('reviews')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('user'), ['This field is required.'])
        self.assertEqual(response.json().get('rating'), ['This field is required.'])
        self.assertEqual(response.json().get('comment'), ['This field is required.'])

    def test_post_review(self):
        url = reverse('reviews')
        data = {
            'user': self.user.id,
            'rating': 5,
            'comment': 'what a great app!'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('user'), self.user.id)
        self.assertEqual(response.json().get('rating'), data.get('rating'))
        self.assertEqual(response.json().get('comment'), data.get('comment'))

    def test_invalid_rating(self):
        url = reverse('reviews')
        data = {
            'user': self.user.id,
            'rating': 7,
            'comment': 'what a great app!'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('rating'), ['Rating value not valid.'])

    def test_no_comment(self):
        url = reverse('reviews')
        data = {
            'user': self.user.id,
            'rating': 5
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('comment'), ['This field is required.'])

    def test_get_empty_reviews(self):
        url = reverse('reviews')

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), list())

    def test_get_reviews(self):
        url = reverse('reviews')

        review = Review.objects.create(user=self.user, rating=5, comment='what a great app!')

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.json()), 0)
        self.assertEqual(response.json()[0].get('user'), review.user.id)
        self.assertEqual(response.json()[0].get('rating'), review.rating)
        self.assertEqual(response.json()[0].get('comment'), review.comment)


class TestAdminReviewAPI(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'insertstrongpassword'
        self.user = User.objects.create_user(
            self.username, 'user@test.com', self.password
        )
        self.user.is_staff = True
        self.user.save()
        for r in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1):
            user = User.objects.create_user(
            'testuser{}'.format(r), 'user{}@test.com'.format(r), 'insertstrongpassword'
            )
            Review.objects.create(user=user, rating=r, comment='Comment {}'.format(r))
        self.client = APIClient()

    def test_list_reviews(self):
        url = reverse('admin-reviews-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.json()), 0)

    def test_csv_reviews(self):
        url = reverse('admin-reviews-csv')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.content), 0)

    def test_stats_reviews(self):
        url = reverse('admin-reviews-stats')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('total_reviews'), MAX_RATING_VALUE)
        self.assertEqual(
            response.json().get('avg_rating'),
            sum([i for i in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1)]) / MAX_RATING_VALUE
        )
        for r in range(MIN_RATING_VALUE, MAX_RATING_VALUE + 1):
            self.assertEqual(response.json().get('total_{}_rates'.format(r)), 1)
            self.assertEqual(response.json().get('avg_{}_rates'.format(r)), r)
