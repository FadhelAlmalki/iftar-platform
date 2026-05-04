from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Initiative, City
from permits.models import Permit
from django.contrib import messages

# All initiatives
def all_initiatives_view(request: HttpRequest):

    initiatives = Initiative.objects.all().order_by('-created_at')
    cities = City.objects.all().order_by('name')

    search_term = request.GET.get('search', '').strip()
    selected_permit_status = request.GET.get('permit_status', '').strip()
    selected_initiative_status = request.GET.get('initiative_status', '').strip()
    selected_city = request.GET.get('city', '').strip().lower()

    if search_term:
        initiatives = initiatives.filter(
            Q(title__icontains=search_term)
            | Q(description__icontains=search_term)
            | Q(place__icontains=search_term)
            | Q(city__name__icontains=search_term)
            | Q(owner__entity_name__icontains=search_term)
        )

    valid_permit_statuses = [choice[0] for choice in Permit.PermitStatus.choices]
    valid_initiative_statuses = [choice[0] for choice in Initiative.InitiativeStatus.choices]
    if selected_permit_status in valid_permit_statuses:
        initiatives = initiatives.filter(permit__permit_status=selected_permit_status)

    if selected_initiative_status in valid_initiative_statuses:
        initiatives = initiatives.filter(init_status=selected_initiative_status)

    valid_city_ids = {str(city.id) for city in cities}
    if selected_city in valid_city_ids:
        initiatives = initiatives.filter(city__id=selected_city)


    #initiatives = initiatives.distinct()

    paginator = Paginator(initiatives, 6)
    page_number = request.GET.get('page')
    initiatives_page = paginator.get_page(page_number)

    filter_query = request.GET.copy()
    filter_query.pop('page', None)

    context = {
        'initiatives': initiatives_page,
        'total_initiatives': paginator.count,
        'cities': cities,
        'permit_statuses': Permit.PermitStatus.choices,
        'initiative_statuses': Initiative.InitiativeStatus.choices,
        'selected_search': search_term,
        'selected_permit_status': selected_permit_status,
        'selected_initiative_status': selected_initiative_status,
        'selected_city': selected_city,
        'query_string': filter_query.urlencode(),
    }
    return render(request, 'initiatives/all_initiatives.html', context)

# Initiative detail
def initiative_detail_view(request: HttpRequest, initiative_id: int):
    initiative = get_object_or_404(Initiative, id=initiative_id)
    
    # try:
    #     permit = initiative.permit
    # except Exception:
    #     permit = None
    permit = Permit.objects.filter(initiative=initiative).first()

    context = {
        'initiative': initiative,
        'permit': permit,
    }
    return render(request, 'initiatives/initiative_detail.html', context)

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


# Admin - review initiative
def review_initiative_view(request: HttpRequest, initiative_id: int, action: str):

    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    if request.user.profile.role != 'admin':
        messages.error(request, 'Access denied.', 'alert-danger')
        return redirect('main:home_view')

    if request.method != 'POST':
        return redirect('main:home_view')

    initiative = get_object_or_404(Initiative, id=initiative_id)

    try:
        if action == 'accept':
            initiative.init_status = 'accepted'
            initiative.save()
            messages.success(request, 'Initiative accepted successfully!', 'alert-success')

        elif action == 'reject':
            initiative.init_status = 'rejected'
            initiative.save()
            messages.warning(request, 'Initiative rejected.', 'alert-warning')

        else:
            messages.error(request, 'Invalid action.', 'alert-danger')

    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong.', 'alert-danger')

    return redirect('initiatives:initiative_detail_view', initiative_id=initiative_id)