from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.memos.models import Memo


class TestMemoModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", email="a@example.com", password="pass1234"
        )

    def test_str_returns_title(self):
        memo = Memo.objects.create(owner=self.user, title="Hello", body="world")
        self.assertEqual(str(memo), "Hello")

    def test_ordering_latest_first(self):
        m1 = Memo.objects.create(owner=self.user, title="A", body="1")
        m2 = Memo.objects.create(owner=self.user, title="B", body="2")
        self.assertEqual(list(Memo.objects.all()), [m2, m1])
