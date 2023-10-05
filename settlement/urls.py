from django.urls import path
from . import views

app_name = 'settlement'
urlpatterns = [
    path('add_student/', views.add_student, name='add_student'),
    path('', views.dormitories, name='dormitories'),
    path('hostel/', views.hostel, name='hostel')
]
