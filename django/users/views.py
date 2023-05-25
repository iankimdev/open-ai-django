from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, SignInForm, UpdateUserForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:signin'))
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

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
    return render(request, 'users/signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        #profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() : # and profile_form.is_valid()
            user_form.save()
            #profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(reverse('users:profile'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        #profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/update_profile.html', {'user_form': user_form}) #'profile_form': profile_form

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users:signin')
