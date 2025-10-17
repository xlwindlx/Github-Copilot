from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Memo
from .forms import MemoForm


class OwnerRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		obj = self.get_object()
		return obj.owner == self.request.user


class MemoListView(LoginRequiredMixin, ListView):
	model = Memo
	paginate_by = 20

	def get_queryset(self):
		return Memo.objects.filter(owner=self.request.user)


class MemoDetailView(LoginRequiredMixin, DetailView):
	model = Memo

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.owner != self.request.user and not obj.is_public:
			# 비공개 문서는 소유자만 볼 수 있음
			return get_object_or_404(Memo, pk=0)  # 의도적으로 404
		return obj


class MemoCreateView(LoginRequiredMixin, CreateView):
	model = Memo
	form_class = MemoForm
	success_url = reverse_lazy("memos:list")

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


class MemoUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
	model = Memo
	form_class = MemoForm
	success_url = reverse_lazy("memos:list")


class MemoDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
	model = Memo
	success_url = reverse_lazy("memos:list")

# Create your views here.
