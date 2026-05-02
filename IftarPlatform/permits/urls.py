from django.urls import path
from . import views

urlpatterns = [
    
    # Organizer
    path('request/<int:initiative_id>/', views.request_permit_view, name='request_permit_view'),
    path('my-permits/', views.my_permits_view, name='my_permits_view'),
    path('detail/<int:permit_id>/', views.permit_detail_view, name='permit_detail_view'),

    # Owner
    path('initiative/<int:initiative_id>/', views.initiative_permit_view, name='initiative_permit_view'),

    # Admin
    path('pending/', views.pending_permits_view, name='pending_permits_view'),
    path('accept/<int:permit_id>/', views.accept_permit_view, name='accept_permit_view'),
    path('reject/<int:permit_id>/', views.reject_permit_view, name='reject_permit_view'),
]