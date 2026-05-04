from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import Initiative, City
from permits.models import Permit
from django.contrib import messages

# All initiatives
def all_initiatives_view(request: HttpRequest):

    initiatives = Initiative.objects.all().order_by('-created_at')
    cities = City.objects.all().order_by('name')

    selected_permit_status = request.GET.get('permit_status', '').strip()
    selected_initiative_status = request.GET.get('initiative_status', '').strip()
    selected_city = request.GET.get('city', '').strip().lower()

    valid_permit_statuses = [choice[0] for choice in Permit.PermitStatus.choices]
    valid_initiative_statuses = [choice[0] for choice in Initiative.InitiativeStatus.choices]
    if selected_permit_status in valid_permit_statuses:
        initiatives = initiatives.filter(permit__status=selected_permit_status)

    if selected_initiative_status in valid_initiative_statuses:
        initiatives = initiatives.filter(init_status=selected_initiative_status)

    valid_city_ids = {str(city.id) for city in cities}
    if selected_city in valid_city_ids:
        initiatives = initiatives.filter(city__id=selected_city)


    #initiatives = initiatives.distinct()

    context = {
        'initiatives': initiatives,
        'cities': cities,
        'permit_statuses': Permit.PermitStatus.choices,
        'initiative_statuses': Initiative.InitiativeStatus.choices,
        'selected_permit_status': selected_permit_status,
        'selected_initiative_status': selected_initiative_status,
        'selected_city': selected_city,
    }
    return render(request, 'initiatives/all_initiatives.html', context)

# Initiative detail
def initiative_detail_view(request: HttpRequest, initiative_id: int):
    return render(request, 'initiatives/initiative_detail.html')

# Add initiative
def add_initiative_view(request: HttpRequest):
    if not (request.user.is_authenticated and request.user.profile.role == 'owner'):
        messages.warning(request, "You do not have permission to add an initiative.", extra_tags='alert-warning')
        return redirect("main:home_view")
    
    # cities = City.objects.all()
    cities = City.objects.filter(is_active=True)

    if request.method == 'POST':
        city_id = request.POST.get("city")
        city = City.objects.get(id=city_id)
        
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