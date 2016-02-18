from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from autofixture import AutoFixture

from browse.models import Review, Professor, School
from new.tests import srs


class BrowseViewsTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.NUM_EVERYTHING = 100

        # AutoFixture(User).create(50)
        # Create reviews, recursively creating models where needed
        AutoFixture(Review, generate_fk=True).create(20)

        self.two_review_types = ["by_school", "by_professor"]
        self.three_review_types = ["by_school_professor"]

    def test_index(self):
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)

    def test_profile_not_logged_in(self):
        resp = self.client.get(reverse("profile"))
        self.assertEqual(resp.status_code, 200)

        # Should be someone else.
        self.assertNotEqual(resp.context["user"].username, self.user.username)

    def test_profile_logged_in(self):
        self.client.login(**self.creds)
        resp = self.client.get(reverse("profile"))

        # Should be feeding it the profile for our user.
        self.assertEqual(resp.context["user"].username, self.user.username)

    def test_profile_specific(self):
        resp = self.client.get(reverse("profile", args=[srs(User).id]))
        self.assertEqual(resp.status_code, 200)

        self.client.login(**self.creds)
        resp = self.client.get(reverse("profile", args=[srs(User).id]))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)

    def test_login_login(self):
        resp = self.client.post(reverse("login"), {
                                "username": self.user.username,
                                "password": self.user.password})
        self.assertEqual(resp.status_code, 200)

    def test_logout(self):
        self.client.login(**self.creds)

        resp = self.client.get(reverse("logout"))
        self.assertEqual(resp.status_code, 302)  # redir to index

        resp = self.client.get(reverse("index"))
        self.assertEqual(str(resp.context["user"]), "AnonymousUser")

    def test_review_specific(self):
        resp = self.client.get(reverse("review", args=[srs(Review).id]))
        self.assertEqual(resp.status_code, 200)

    def test_reviews(self):
        resp = self.client.get(reverse("reviews"))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_page(self):
        resp = self.client.get(reverse("reviews", kwargs={"page": 1}))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_by_type(self):
        for type in self.two_review_types:
            resp = self.client.get(reverse("reviews",
                                   kwargs={"page": 1, "type": type,
                                           "first_id": 1}))
            self.assertEqual(resp.status_code, 200)

        for type in self.three_review_types:
            resp = self.client.get(reverse("reviews",
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
