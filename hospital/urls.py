from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main Dashboard and Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    
    # Booking & Tokens
    path('get-token/<int:doctor_id>/', views.generate_token, name='generate_token'), 
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    
    # Utilities
    path('bmi/', views.bmi_calculator, name='bmi_calculator'), 
    path('ambulances/', views.ambulance_list, name='ambulance_list'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),

    # Authentication
    path('signup/', views.signup, name='signup'), # Fix: 'signup_view' ki jagah sirf 'signup'
    path('login/', auth_views.LoginView.as_view(template_name='hospital/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('login-redirect/', views.login_redirect_dispatch, name='login_redirect'),
    
]


