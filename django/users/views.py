from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, SignInForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Profile

User = get_user_model()
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = SignUpForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'User created successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'message': 'Signup failed', 'errors': errors}, status=400)
    else:
        form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = SignInForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'message': 'Invalid username or password'}, status=400)
        else:
            return JsonResponse({'message': 'Form data is invalid'}, status=400)
    else:
        form = SignInForm()
    return render(request, 'users/signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

@login_required
def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        data = json.loads(request.body)
        user_form = UpdateUserForm(data, instance=user)
        profile_form = UpdateProfileForm(data, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return JsonResponse({'success': True, 'message': 'Your profile is updated successfully'})
        else:
            return JsonResponse({'success': False, 'errors': user_form.errors})
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=profile)

    return render(request, 'users/update-profile.html', {'user_form': user_form, 'profile_form': profile_form})



class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = '/users/signin/' 

class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/user-delete.html'
    success_url = reverse_lazy('users:signin')
    success_message = "Your account has been deleted successfully"

    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.delete()
        self.request.session.flush()
        messages.success(self.request, self.success_message)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True})
        else:
            return self.get_success_url()
