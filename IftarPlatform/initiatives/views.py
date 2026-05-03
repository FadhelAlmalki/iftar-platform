from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import Initiative, City
from django.contrib import messages

def all_initiatives_view(request: HttpRequest):
    #initiatives = Initiative.objects.all()
    return render(request, 'initiatives/all_initiatives.html')

def initiative_detail_view(request: HttpRequest, initiative_id: int):
    return render(request, 'initiatives/initiative_detail.html')

# Add initiative
def add_initiative_view(request: HttpRequest):
    cities = City.objects.all()

    city_id = request.POST.get("city")
    city = City.objects.get(id=city_id)

    if not ( request.user.is_authenticated and request.user.profile.role == 'owner'):
        messages.warning(request, "You do not have permission to add an initiative.", extra_tags='alert-warning')
        return redirect("main:home_view")

    if request.method == 'POST':
        new_initiative = Initiative(owner=request.user.profile,
                                    title = request.POST.get('title'),
                                   description = request.POST.get('description'),
                                   city = city,
                                   place = request.POST.get('place'),
                                   image = request.FILES.get('image'),
                                   starts_at = request.POST.get('starts_at'),
                                   ends_at = request.POST.get('ends_at'),
                        )
        new_initiative.save()
        return redirect("main:home_view")
    return render(request, 'initiatives/add_initiative.html', {'cities': cities})