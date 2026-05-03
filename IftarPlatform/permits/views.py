from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Permit

# Create your views here.



def request_permit_view(request: HttpRequest):
    return render(request, 'permits/request_permit.html')

def my_permits_view(request: HttpRequest):
    return render(request, 'permits/my_permits.html')

def permit_detail_view(request: HttpRequest):
    return render(request, 'permits/permit_detail.html')

def initiative_permit_view(request: HttpRequest):
    return redirect('permits:initiative_permit.html')

def pending_permits_view(request: HttpRequest):
    return render(request, 'permits/pending_permits.html')

def accept_permit_view(request: HttpRequest):
    return redirect('permits:pending_permits_view')

def reject_permit_view(request: HttpRequest):
    return redirect('permits:pending_permits_view')
