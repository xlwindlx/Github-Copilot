from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestAuthFlows(TestCase):
    def test_register_login_logout(self):
        # Register
        resp = self.client.post(
            reverse("users:register"),
            data={
                "username": "alice",
                "email": "a@example.com",
                "password": "pass1234",
                "password_confirm": "pass1234",
            },
            follow=False,
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="alice").exists())

        # Logout
        resp = self.client.get(reverse("users:logout"), follow=False)
        self.assertEqual(resp.status_code, 302)

        # Login
        resp = self.client.post(
            reverse("users:login"),
            data={"username": "alice", "password": "pass1234"},
            follow=False,
        )
        self.assertEqual(resp.status_code, 302)
