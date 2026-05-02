from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_initiatives_view, name='all_initiatives_view'),
]