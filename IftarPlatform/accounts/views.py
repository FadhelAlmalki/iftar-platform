from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile

# Create your views here.

def signup_view(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect('main:home_view')

    if request.method == 'POST':
        try:
            
            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                )
            new_user.save()

        
            profile = Profile(
                user=new_user,
                role=request.POST['role'],
                entity_name=request.POST['entity_name'],
                rep_id=request.POST['rep_id'],
                about=request.POST['about'],
                avatar=request.FILES.get('avatar', Profile.avatar.field.get_default()),
            )
            profile.save()

            messages.success(request, 'Registered successfully!', 'alert-success')
            return redirect('accounts:signin_view')

        except Exception as e:
            messages.error(request, f'Username already exists! {str(e)}', 'alert-danger')
            print(e)

    return render(request, 'accounts/sign_up.html')

def signin_view(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect('home_view')

    if request.method == 'POST':
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'],)

        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully!', 'alert-success')
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Invalid username or password.', 'alert-danger')

    return render(request, 'accounts/sign_in.html')


def logout_view(request: HttpRequest):
    logout(request)
    messages.warning(request, 'Logged out successfully.', 'alert-warning')
    return redirect(request.GET.get('next', '/'))


def user_profile_view(request: HttpRequest, user_name: str):

    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    profile_user = get_object_or_404(User, username=user_name)
    profile = get_object_or_404(Profile, user=profile_user)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'profile_user': profile_user,
    })