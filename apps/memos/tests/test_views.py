from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.memos.models import Memo


class TestMemoViews(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(
            username="alice", email="a@example.com", password="pass1234"
        )
        self.bob = User.objects.create_user(
            username="bob", email="b@example.com", password="pass1234"
        )

    def test_list_requires_login(self):
        resp = self.client.get(reverse("memos:list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/users/login/", resp.url)

    def test_owner_sees_only_own_memos(self):
        Memo.objects.create(owner=self.alice, title="A1", body="...")
        Memo.objects.create(owner=self.bob, title="B1", body="...")
        self.client.login(username="alice", password="pass1234")
        resp = self.client.get(reverse("memos:list"))
        self.assertContains(resp, "A1")
        self.assertNotContains(resp, "B1")

    def test_private_detail_not_accessible_by_non_owner(self):
        memo = Memo.objects.create(owner=self.alice, title="Secret", body="...", is_public=False)
        self.client.login(username="bob", password="pass1234")
        resp = self.client.get(reverse("memos:detail", args=[memo.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_create_sets_owner(self):
        self.client.login(username="alice", password="pass1234")
        resp = self.client.post(
            reverse("memos:create"),
            data={"title": "New", "body": "txt", "is_public": True},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        memo = Memo.objects.get(title="New")
        self.assertEqual(memo.owner, self.alice)

    def test_edit_denied_for_non_owner(self):
        memo = Memo.objects.create(owner=self.alice, title="A1", body="...")
        self.client.login(username="bob", password="pass1234")
        resp = self.client.post(
            reverse("memos:edit", args=[memo.pk]),
            data={"title": "Hack", "body": "x"},
        )
        # Should 404 because queryset filters by owner
        self.assertEqual(resp.status_code, 404)
