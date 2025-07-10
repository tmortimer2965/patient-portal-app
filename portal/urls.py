from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('appointments/', views.appointment_list_view, name='appointment_list'),
    path('appointments/new/', views.appointment_create_view, name='appointment_create_view'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('messages/', views.message_list_view, name='message_list'),
    path('my-patients/', views.doctor_patients_view, name='doctor_patients'),
    path('appointments/<int:appointment_id>/notes', views.edit_notes_view, name='edit_notes')
]