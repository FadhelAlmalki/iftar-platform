from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Permit

# Create your views here.


#ِOrganizer
def request_permit_view(request: HttpRequest, initiative_id: int):
    return render(request, 'permits/request_permit.html')
#ِOrganizer
def my_permits_view(request: HttpRequest):
    return render(request, 'permits/my_permits.html')
#ِOrganizer
def permit_detail_view(request: HttpRequest, permit_id: int):
    return render(request, 'permits/permit_detail.html')
#Owner
def initiative_permit_view(request: HttpRequest, initiative_id: int):
    return render(request, 'permits/initiative_permit.html')
#ِAdmin
def pending_permits_view(request: HttpRequest):
    return render(request, 'permits/pending_permits.html')
#ِAdmin
def review_permit_view(request: HttpRequest, permit_id: int, action: str):
    return redirect('permits:pending_permits_view')
