from django.urls import path
from . import views

urlpatterns = [
    
    path('all/', views.all_permits_view, name='all_permits_view'),
    path('detail/<int:permit_id>/', views.permit_detail_view, name='permit_detail_view'),
    
    
    path('apply/<int:initiative_id>/', views.apply_for_permit_view, name='apply_for_permit_view'),
    
    #for Admin (accept or reject)
    path('update-status/<int:permit_id>/<str:status>/', views.update_permit_status_view, name='update_permit_status_view'),
    
    # for Owner and Organizer
    path('my-permits/', views.my_permits_view, name='my_permits_view'),
]