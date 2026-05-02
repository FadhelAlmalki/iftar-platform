from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Profile

# Create your views here.
VALID_ROLES = ['owner', 'organizer']


def role_select_view(request: HttpRequest, action: str):
    """صفحة اختيار الدور (action = signup أو signin)"""
    if action not in ['signup', 'signin']:
        return redirect('home_view')
    
    return render(request, 'accounts/role_select.html', {'action': action})


def signup_view(request: HttpRequest, role: str):
    """تسجيل حساب جديد بناءً على الدور"""
    
    if role not in VALID_ROLES:
        messages.error(request, 'Invalid role selected.', extra_tags='alert-danger')
        return redirect('home_view')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rep_id = request.POST.get('rep_id')
        entity_name = request.POST.get('entity_name')
        about = request.POST.get('about')
        image = request.FILES.get('image')
        
        # check username if exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.', extra_tags='alert-danger')
            return redirect('signup_view', role=role)
        
        # check email if exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.', extra_tags='alert-danger')
            return redirect('signup_view', role=role)
        
        # create user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        
        # create profile
        Profile.objects.create(
            user=user,
            role=role,
            rep_id=rep_id,
            entity_name=entity_name,
            about=about,
            image=image
        )
        
        
        login(request, user)
        messages.success(request, f'Welcome {first_name}! Your account has been created.', extra_tags='alert-success')
        return redirect('dashboard_view')
    
    return render(request, 'accounts/signup.html', {'role': role})


def signin_view(request: HttpRequest, role: str):
    """Sign In depend on role"""
    
    if role not in VALID_ROLES:
        messages.error(request, 'Invalid role selected.', extra_tags='alert-danger')
        return redirect('home_view')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # التحقق من إن دور المستخدم يطابق الـ URL
            if hasattr(user, 'profile') and user.profile.role == role:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!', extra_tags='alert-success')
                return redirect('dashboard_view')
            else:
                messages.error(request, f'This account is not registered as {role}.', extra_tags='alert-danger')
        else:
            messages.error(request, 'Invalid username or password.', extra_tags='alert-danger')
    
    return render(request, 'accounts/signin.html', {'role': role})


def logout_view(request: HttpRequest):
    """Logging Out"""
    logout(request)
    messages.success(request, 'You have been logged out.', extra_tags='alert-success')
    return redirect('home_view')


# def dashboard_view(request: HttpRequest):
#     """redirect to dashboard depend on role"""
    
#     if not request.user.is_authenticated:
#         messages.error(request, 'Please sign in first.', extra_tags='alert-danger')
#         return redirect('home_view')
    
#     role = request.user.profile.role
    
#     if role == 'owner':
#         return render(request, 'accounts/owner_dashboard.html')
#     elif role == 'organizer':
#         return render(request, 'accounts/organizer_dashboard.html')
#     elif role == 'admin':
#         return render(request, 'accounts/admin_dashboard.html')
    
#     return redirect('home_view')