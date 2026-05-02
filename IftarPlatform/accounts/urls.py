from django.urls import path
from . import views

app_name="accounts"

urlpatterns=[

    path('role-select/<str:action>/', views.role_select_view, name='role_select_view'),
    
    path('signup/<str:role>/', views.signup_view, name='signup_view'),
    path('signin/<str:role>/', views.signin_view, name='signin_view'),
    path('logout/', views.logout_view, name='logout_view'),
]