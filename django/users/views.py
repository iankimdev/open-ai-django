from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, SignInForm
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:signin'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('http://127.0.0.1:8000/')  # Redirect to the home page after successful login
            else:
                form.add_error(None, 'Invalid username or password')  # Add a form-level error message
    else:
        form = SignInForm()
    # Add provider_login_url to the context
    return render(request, 'signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')