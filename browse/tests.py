from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from autofixture import AutoFixture

from browse.models import FieldCategory, Field, Department, Review, Professor,\
    School, ReviewVote, Course
from new.tests import srs
from django.utils import formats

import json


class TestBrowseViews(TestCase):
    @classmethod
    def setUpClass(cls):
        # Every test needs access to the request factory.
        cls.factory = RequestFactory()
        cls.NUM_EVERYTHING = 100
        models = [User, FieldCategory, Field, School, Department, Course,
                  Professor, Review, ReviewVote]

        for m in models:
            AutoFixture(m).create(20)

        cls.two_review_types = ["by_school", "by_professor"]
        cls.three_review_types = ["by_school_professor"]
        super(TestBrowseViews, cls).setUpClass()

        cls.creds = {"username": "test_user", "password": "tesT_pass"}

    def setUp(self):
        User.objects.create_user(**self.creds).save()

    def test_home(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)

    def test_profile_not_logged_in(self):
        resp = self.client.get(reverse("profile"))
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_profile_logged_in(self):
        url = reverse("profile")
        req = self.factory.get(url)

        req.user = srs(User)

        resp = resolve(url).func(req)

        self.assertEqual(resp.status_code, 200)

    def test_profile_specific(self):
        resp = self.client.get(reverse("profile", args=[srs(User).id]))
        self.assertEqual(resp.status_code, 200)

        self.client.login(**self.creds)
        resp = self.client.get(reverse("profile", args=[srs(User).id]))
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

    def test_login_login(self):
        url = reverse("login")
        req = self.factory.post(url, json.dumps(self.creds),
                                content_type="text/json")

        # Set up our session
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        resp = resolve(url).func(req)

        # Redirect to index
        self.assertEqual(resp.status_code, 200)

    """
    def test_logout(self):
        url = reverse("login")
        req = self.factory.post(url, {"username": self.creds["username"],
                                      "password": self.creds["password"]})

        resp = resolve(url).func(req)

        url = reverse("logout")
        req = self.factory.get(url)

        req.user = srs(User)
        resp = resolve(url).func(req)

        self.assertEqual(str(resp.context["user"].username), "")
    """

    def test_review_specific(self):
        resp = self.client.get(reverse("review", args=[srs(Review).id]))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_overview(self):
        resp = self.client.get(reverse("reviews"))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_page(self):
        resp = self.client.get(reverse("reviews", kwargs={"page": 1}))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_by_type(self):
        for type in self.two_review_types:
            resp = self.client.get(reverse("reviews_by_type_one",
                                   kwargs={"page": 1, "type": type,
                                           "first_id": 1}))
            self.assertEqual(resp.status_code, 200)

        for type in self.three_review_types:
            resp = self.client.get(reverse("reviews_by_type_two",
                                   kwargs={"page": 1, "type": type,
                                           "first_id": 1,
                                           "second_id": 1}))
            self.assertEqual(resp.status_code, 200)

    def test_schools(self):
        resp = self.client.get(reverse("schools"))
        self.assertEqual(resp.status_code, 200)

    def test_school_specific(self):
        resp = self.client.get(reverse("school",
                               args=[srs(School).id]))
        self.assertEqual(resp.status_code, 200)

    def test_professor(self):
        resp = self.client.get(reverse("professors"))
        self.assertEqual(resp.status_code, 200)

    def test_professor_specific(self):
        resp = self.client.get(reverse("professor",
                               args=[srs(Professor).id]))
        self.assertEqual(resp.status_code, 200)


class ReviewContent(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.NUM_EVERYTHING = 100

        # AutoFixture(User).create(50)
        # Create reviews, recursively creating models where needed
        AutoFixture(Review, generate_fk=True).create(20)

    def test_home(self):
        """
        Index should show at least five (20 total) reviews.
        """
        resp = self.client.get(reverse("home"))

        self.assertIn("review_votes", resp.context)
        self.assertGreaterEqual(len(resp.context["review_votes"]), 5)
        content = resp.content.decode()

        for review, vote in resp.context["review_votes"]:
            # Check that all information is there
            self.assertIn(review.target.last_name, content)
            self.assertIn(review.target.first_name, content)
            self.assertIn(review.course.name, content)
            self.assertIn(review.owner.first_name, content)
            self.assertIn(review.owner.last_name, content)

            # Check for a link to the full review
            self.assertIn(reverse('review', args=[review.id]), content)

    def test_reviews(self):
        """
        Should list every single review.
        """
        resp = self.client.get(reverse("reviews"))

        self.assertIn("review_votes", resp.context)
        self.assertGreaterEqual(len(resp.context["review_votes"]), 5)
        content = resp.content.decode()

        # Check the last 5
        for review in Review.objects.order_by('-created_ts')[0:5]:
            # Check that all information is there
            self.assertIn(review.target.last_name, content)
            self.assertIn(review.target.first_name, content)
            self.assertIn(review.course.name, content)
            self.assertIn(review.owner.first_name, content)
            self.assertIn(review.owner.last_name, content)

            # Check for a link to the full review
            self.assertIn(reverse('review', args=[review.id]), content)

    def test_view_review(self):
        """
        Should have individual review pages for every review with all
        required information.
        """
        for review in Review.objects.all():
            resp = self.client.get(reverse("review", args=[review.id]))

            self.assertEqual(resp.status_code, 200)
            self.assertIn("review", resp.context)
            content = resp.content.decode()

            # check for all professor details
            self.assertIn(review.target.last_name, content)
            self.assertIn(review.target.first_name, content)
            self.assertIn(review.course.name, content)
            self.assertIn(str(review.course.number), content)
            self.assertIn(review.course.department.name, content)

            # Check for reviewer details
            self.assertIn(review.owner.first_name, content)
            self.assertIn(review.owner.last_name, content)
            self.assertIn(review.owner.username, content)
            self.assertIn(formats.date_format(review.created_ts,
                                              "DATETIME_FORMAT"), content)
            if review.updated_ts:
                self.assertIn(formats.date_format(review.updated_ts,
                                                  "DATETIME_FORMAT"), content)
