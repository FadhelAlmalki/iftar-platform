from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Permit

# Create your views here.



def all_permits_view(request: HttpRequest):
    """ View for Admin to see all permit requests in the system """

    return render(request, 'permits/all_permits.html')

def permit_detail_view(request: HttpRequest, permit_id: int):
    """ View to see the full details of a specific permit (PDF, QR, Status) """

    return render(request, 'permits/permit_detail.html')

def apply_for_permit_view(request: HttpRequest, initiative_id: int):
    """ View for Organizers to submit a new permit request for a specific initiative """

    return render(request, 'permits/apply_permit.html')

def update_permit_status_view(request: HttpRequest, permit_id: int, status: str):
    """ View for Admin to change permit status (accepted/rejected) """

    return redirect('permits:all_permits_view')

def my_permits_view(request: HttpRequest):
    """ View for Owners or Organizers to see their own related permits """
    
    return render(request, 'permits/my_permits.html')
