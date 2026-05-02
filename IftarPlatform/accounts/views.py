from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile

# Create your views here.

def signup_view(request: HttpRequest, role: str):
    """ Handle user registration for specific roles (owner/organizer) """
    if request.method == 'POST':
        # Get data from POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rep_id = request.POST.get('rep_id')
        entity_name = request.POST.get('entity_name')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html', {'role': role})

        # Create User object
        new_user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create Profile object linked to the user
        Profile.objects.create(
            user=new_user,
            role=role,
            rep_id=rep_id,
            entity_name=entity_name
        )
        
        login(request, new_user)
        messages.success(request, f"Welcome! Your account as {role} has been created.")
        return redirect('main:home')

    return render(request, 'signup.html', {'role': role})

def signin_view(request: HttpRequest, role: str):
    """ Handle login for a specific role """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user's profile role matches the URL role
            if user.profile.role == role:
                login(request, user)
                messages.success(request, f"Logged in successfully as {role}.")
                return redirect('main:home')
            else:
                messages.error(request, f"This account is not registered as {role}.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'signin.html', {'role': role})


def user_profile_view(request: HttpRequest):
    """ Display the logged-in user's profile information """
    if not request.user.is_authenticated:
        return redirect('accounts:signin_view', role='owner')
    
    # Context contains profile data via the OneToOne relationship
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request: HttpRequest):
    """ Terminate user session """
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('accounts:signin_view', role='owner') # Default redirect