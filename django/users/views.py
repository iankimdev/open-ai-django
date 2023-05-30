from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse_lazy
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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, SignInSerializer, ProfileSerializer, UpdateProfileSerializer, UpdateUserSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


@csrf_exempt
@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'email': serializer.data['email'],
                'username': serializer.data['username'],
                'message': 'User created successfully'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = UserSerializer()
        return render(request, 'users/signup.html')
    
@csrf_exempt
@api_view(['GET', 'POST'])
def signin(request):
    serializer = SignInSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        else:
            return Response({'message': 'Invalid username or password'}, status=400)
    else:
        return render(request, 'users/signin.html')

def signout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
@login_required
@api_view(['GET', 'PUT'])
def profile(request):
    
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    if request.method == 'PUT':
        user_serializer = UpdateUserSerializer(data=request.data, instance=user)
        profile_serializer = UpdateProfileSerializer(data=request.data, instance=profile)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response({'success': True, 'message': 'Your profile is updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user_serializer = UserSerializer(instance=user)
        profile_serializer = ProfileSerializer(instance=profile)
    return render(request, 'users/profile.html', {'user_data': user_serializer.data, 'profile_data': profile_serializer.data})



class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'users/password-change.html')

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(context={'request': request}, data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password1 = serializer.validated_data.get("new_password1")
            new_password2 = serializer.validated_data.get("new_password2")

            if not user.check_password(old_password):
                return Response({"old_password": ["Invalid old password."]}, status=status.HTTP_400_BAD_REQUEST)

            if new_password1 != new_password2:
                return Response({"new_password2": ["The new passwords do not match."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password1)
            user.save()

            response = {
                'success': True,
                'message': "Successfully changed your password"
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'users/delete.html')
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        request.session.flush()

        return Response({"message": "Your account has been deleted successfully", "success": True})
