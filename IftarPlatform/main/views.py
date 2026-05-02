from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Contact

def home_view(request: HttpRequest):
    return render(request, 'main/index.html')

def contact_view(request: HttpRequest):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        messages.success(request, 'Your message has been sent successfully!', extra_tags='alert-success')
        return redirect('main:contact_view')
    

    return render(request, 'main/contact.html')
