from django.http import HttpRequest
from django.shortcuts import render

def all_initiatives_view(request: HttpRequest):
    return render(request, 'initiatives/all_initiatives.html')