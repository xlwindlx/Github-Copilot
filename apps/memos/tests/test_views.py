from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.memos.models import Memo
from apps.memos.views import MemoListView, MemoDetailView, MemoUpdateView
from django.http import Http404


class TestMemoViews(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(
            username="alice", email="a@example.com", password="pass1234"
        )
        self.bob = User.objects.create_user(
            username="bob", email="b@example.com", password="pass1234"
        )
        self.rf = RequestFactory()

    def test_list_requires_login(self):
        resp = self.client.get(reverse("memos:list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/users/login/", resp.url)

    def test_owner_sees_only_own_memos(self):
        m_a = Memo.objects.create(owner=self.alice, title="A1", body="...")
        Memo.objects.create(owner=self.bob, title="B1", body="...")
        req = self.rf.get(reverse("memos:list"))
        req.user = self.alice
        view = MemoListView()
        view.request = req
        qs = view.get_queryset()
        self.assertIn(m_a, list(qs))
        self.assertTrue(all(m.owner == self.alice for m in qs))

    def test_private_detail_not_accessible_by_non_owner(self):
        memo = Memo.objects.create(owner=self.alice, title="Secret", body="...", is_public=False)
        req = self.rf.get(reverse("memos:detail", args=[memo.pk]))
        req.user = self.bob
        view = MemoDetailView()
        view.request = req
        view.kwargs = {"pk": memo.pk}
        with self.assertRaises(Http404):
            view.get_object()

    def test_create_sets_owner(self):
        self.client.login(username="alice", password="pass1234")
        resp = self.client.post(
            reverse("memos:create"),
            data={"title": "New", "body": "txt", "is_public": True, "category": "work"},
            follow=False,
        )
        self.assertEqual(resp.status_code, 302)
        memo = Memo.objects.get(title="New")
        self.assertEqual(memo.owner, self.alice)
        self.assertEqual(memo.category, "work")

    def test_edit_denied_for_non_owner(self):
        memo = Memo.objects.create(owner=self.alice, title="A1", body="...")
        req = self.rf.post(reverse("memos:edit", args=[memo.pk]), data={"title": "Hack", "body": "x"})
        req.user = self.bob
        view = MemoUpdateView()
        view.request = req
        view.kwargs = {"pk": memo.pk}
        with self.assertRaises(Http404):
            view.get_object()

    def test_category_optional_and_filtering(self):
        # Create without category
        self.client.login(username="alice", password="pass1234")
        m1 = Memo.objects.create(owner=self.alice, title="C1", body="...")
        m2 = Memo.objects.create(owner=self.alice, title="C2", body="...", category="daily")

        # Later add category to m1 (avoid template rendering by not following)
        resp = self.client.post(
            reverse("memos:edit", args=[m1.pk]),
            data={"title": m1.title, "body": m1.body, "category": "personal", "is_public": False},
            follow=False,
        )
        self.assertEqual(resp.status_code, 302)
        m1.refresh_from_db()
        self.assertEqual(m1.category, "personal")

        # Filter by 'daily' via get_queryset
        req = self.rf.get(reverse("memos:list"), {"category": "daily"})
        req.user = self.alice
        view = MemoListView()
        view.request = req
        qs = view.get_queryset()
        titles = {m.title for m in qs}
        self.assertIn("C2", titles)
        self.assertNotIn("C1", titles)
