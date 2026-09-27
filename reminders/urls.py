from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Users / Patients
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Medicines
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_add, name='medicine_add'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),

    # Dosages
    path('dosages/add/', views.dosage_add, name='dosage_add'),

    # Schedules
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/add/', views.schedule_add, name='schedule_add'),
    path('schedules/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('schedules/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),

    # Logs
    path('logs/', views.log_list, name='log_list'),
    path('logs/<int:pk>/status/', views.log_update_status, name='log_update_status'),
    path('logs/generate/', views.generate_todays_reminders, name='generate_reminders'),
]
