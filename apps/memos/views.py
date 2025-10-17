from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
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
		qs = Memo.objects.filter(owner=self.request.user)
		category = self.request.GET.get("category")
		if category:
			qs = qs.filter(category=category)
		return qs


class MemoDetailView(LoginRequiredMixin, DetailView):
	model = Memo

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.owner != self.request.user and not obj.is_public:
			# 비공개 문서는 소유자만 볼 수 있음
			raise Http404("Not found")
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
    
	def get_queryset(self):
		# 소유자 문서만 편집 가능
		return Memo.objects.filter(owner=self.request.user)


class MemoDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
	model = Memo
	success_url = reverse_lazy("memos:list")
    
	def get_queryset(self):
		# 소유자 문서만 삭제 가능
		return Memo.objects.filter(owner=self.request.user)

# Create your views here.
