from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login and logout views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('register/', views.register, name='register'),
    
    # Parent dashboard
    path('dashboard/', views.parent_dashboard, name='parent_dashboard'),
]
