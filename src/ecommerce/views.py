from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import  LoginForm, RegisterForm

#render pages


#render home page
def home_page(request):
	context = {
		"content": "Shop by Category",
	}
	if request.user.is_authenticated:
		context["premium_content"] = "YEAHHHHH"
	return render(request, "home_page.html", context)

#render profile page
def profile_page(request):
	return render(request,"home_page.html" )

#render login page
def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
		"form": form
	}
	print("User logged in")
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)	
			return redirect("/")
		else:
			print("Error")
	return render(request, "auth/login.html", context)

User = get_user_model()

#render register page
def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form": form
	}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		new_user = authenticate (username = username, password = password)
		print(new_user)
		login(request, new_user)
		return render(request, "home_page.html", context)
		
	return render(request, "auth/register.html", context)

#render logout page
def logout_page (request):
	logout (request)
	context = {
		"title":"Hello World!",
		"content":"Welcome to the homepage.",
	}
	return render(request, "home_page.html", context)
