from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.utils import timezone

from .utils import generate_qr_code, generate_pdf
from .models import Permit
from initiatives.models import Initiative

# Create your views here.


#ِOrganizer
def request_permit_view(request: HttpRequest, initiative_id: int):

    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    if request.user.profile.role != 'organizer':
        messages.error(request, 'Only organizers can request permits.', 'alert-danger')
        return redirect('main:home_view')

    if request.method != 'POST':
        return redirect('main:home_view')

    initiative = get_object_or_404(Initiative, id=initiative_id)

    if initiative.init_status != 'accepted':
        messages.error(request, 'This initiative is not approved yet.', 'alert-danger')
        return redirect('initiatives:initiative_detail_view', initiative_id=initiative_id)

    permit_exists = Permit.objects.filter(initiative=initiative).exists()
    if permit_exists:
        messages.error(request, 'This initiative already has a permit.', 'alert-danger')
        return redirect('initiatives:initiative_detail_view', initiative_id=initiative_id)

    try:
        Permit.objects.create(
            organizer=request.user.profile,
            initiative=initiative,
            permit_number=f"IFT-{initiative_id}-{request.user.id}",
            starts_at=initiative.starts_at,
            expires_at=initiative.ends_at,
            permit_status='pending',
        )
        messages.success(request, 'Permit requested successfully!', 'alert-success')
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong.', 'alert-danger')

    return redirect('initiatives:initiative_detail_view', initiative_id=initiative_id)

#ِOrganizer
def my_permits_view(request: HttpRequest):

    # Check if user is authenticated and is an organizer
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    if request.user.profile.role != 'organizer':
        messages.error(request, 'Only available for Organizer.', 'alert-danger')
        return redirect('main:home_view')

    permits = Permit.objects.filter(
        organizer=request.user.profile
    ).order_by('-created_at')

    return render(request, 'permits/my_permits.html', {'permits': permits})

#ِOrganizer
def permit_detail_view(request: HttpRequest, permit_id: int):

    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    permit = get_object_or_404(Permit, id=permit_id)

    # Check if user is the owner of the permit
    if permit.organizer != request.user.profile:
        messages.error(request, 'Access denied.', 'alert-danger')
        return redirect('permits:my_permits_view')

    return render(request, 'permits/permit_detail.html', {'permit': permit})

#Owner
def initiative_permit_view(request: HttpRequest, initiative_id: int):

    # Check if user is authenticated and is an owner
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    if request.user.profile.role != 'owner':
        messages.error(request, 'Access denied.', 'alert-danger')
        return redirect('main:home_view')

    initiative = get_object_or_404(Initiative, id=initiative_id)

    # Check if the initiative belongs to the owner
    if initiative.owner != request.user.profile:
        messages.error(request, 'Access denied.', 'alert-danger')
        return redirect('main:home_view')

    # Get the permit for this initiative
    permit = Permit.objects.filter(initiative=initiative).first()

    return render(request, 'permits/initiative_permit.html', {
        'initiative': initiative,
        'permit': permit,
    })

#ِAdmin
def pending_permits_view(request: HttpRequest):

    # Check if user is authenticated and is an admin
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    if request.user.profile.role != 'admin':
        messages.error(request, 'Access denied.', 'alert-danger')
        return redirect('main:home_view')

    permits = Permit.objects.filter(permit_status='pending').order_by('-created_at')

    return render(request, 'permits/pending_permits.html', {'permits': permits})

#ِAdmin
def review_permit_view(request: HttpRequest, permit_id: int, action: str):

    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in first.', 'alert-danger')
        return redirect('accounts:signin_view')

    if request.user.profile.role != 'admin':
        messages.error(request, 'Access denied.', 'alert-danger')
        return redirect('main:home_view')

    if request.method != 'POST':
        return redirect('main:home_view')

    permit = get_object_or_404(Permit, id=permit_id)

    try:
        if action == 'accept':
            permit.permit_status = 'accepted'
            permit.generated_at = timezone.now()
            generate_qr_code(permit)
            generate_pdf(permit)
            permit.save()
            # TODO: generate QR + PDF
            messages.success(request, 'Permit accepted successfully!', 'alert-success')

        elif action == 'reject':
            permit.permit_status = 'rejected'
            permit.save()
            messages.warning(request, 'Permit rejected.', 'alert-warning')

        else:
            messages.error(request, 'Invalid action.', 'alert-danger')

    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong.', 'alert-danger')

    return redirect('initiatives:initiative_detail_view', initiative_id=permit.initiative.id)
