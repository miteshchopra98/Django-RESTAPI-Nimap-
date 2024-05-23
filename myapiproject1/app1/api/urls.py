from django.contrib import admin
from django.urls import include, path
from app1.api import views

urlpatterns = [
    path('home/', views.Home, name='home'),
    path('clients/', views.client_list, name='client-list'),
    path('clients/<int:pk>/', views.client_details, name='client-detail'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.project_details, name='project-detail'),
    path('myprojects/', views.my_projects, name = 'myprojects'),
]