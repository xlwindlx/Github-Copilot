from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegisterForm


class UserLoginView(LoginView):
	template_name = "users/login.html"


class UserLogoutView(LogoutView):
	next_page = reverse_lazy("memos:list")


def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data["password"])
			user.save()
			login(request, user)
			return redirect("memos:list")
	else:
		form = RegisterForm()
	return render(request, "users/register.html", {"form": form})

# Create your views here.
