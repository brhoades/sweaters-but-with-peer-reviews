from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class BrowseViewsTestCase(TestCase):
    fixtures = ["general_test_data.json"]

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.creds = {"username": "jason", "password": "top_secret"}
        self.user = User.objects.\
            create_user(**self.creds,
                        email="jsholm@mst.edu", first_name="Jason",
                        last_name="Holm")

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
        resp = self.client.get(reverse("profile", kwargs={"id": 2}))
        self.assertEqual(resp.status_code, 200)

        self.client.login(**self.creds)
        resp = self.client.get(reverse("profile", kwargs={"id": 2}))
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
        resp = self.client.get(reverse("review", kwargs={"review_id": 2}))
        self.assertEqual(resp.status_code, 200)

    def test_reviews(self):
        resp = self.client.get(reverse("review", kwargs={"review_id": 2}))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_(self):
        resp = self.client.get(reverse("reviews", kwargs={"page": 1}))
        self.assertEqual(resp.status_code, 200)
