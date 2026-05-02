from django.http import HttpRequest
from django.shortcuts import render
from django.contrib import messages

def all_initiatives_view(request: HttpRequest):
    return render(request, 'initiatives/all_initiatives.html')

def initiative_detail_view(request: HttpRequest, initiative_id: int):
    return render(request, 'initiatives/initiative_detail.html')

def add_initiative_view(request: HttpRequest):
    return render(request, 'initiatives/add_initiative.html')