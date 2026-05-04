from django.urls import path
from . import views

app_name = 'initiatives'

urlpatterns = [
    path('all/', views.all_initiatives_view, name='all_initiatives_view'),
    path('<int:initiative_id>/detail/', views.initiative_detail_view, name='initiative_detail_view'),
    path('new/', views.add_initiative_view, name='add_initiative_view'),

    #Admin
    path('<int:initiative_id>/review/<str:action>/', views.review_initiative_view, name='review_initiative_view'),
]