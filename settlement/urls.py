from django.urls import path
from . import views

app_name = 'settlement'
urlpatterns = [
    # path('<int:hostel_number>/', views.hostel, name='hostel'),
    # path('<int:hostel_number/floor_number>', views.floor, name='floor'),
    path('add_student/', views.forms, name='add_student'),
    path('', views.dormitories, name='dormitories'),
    path('hostel/seven/1/', views.Hostel_seven.one, name='one'),
    path('hostel/seven/2/', views.Hostel_seven.two, name='two'),
    path('hostel/seven/3/', views.Hostel_seven.three, name='three'),
    path('hostel/seven/4/', views.Hostel_seven.four, name='four'),
    path('hostel/seven/5/', views.Hostel_seven.five, name='five'),
    path('hostel/seven/6/', views.Hostel_seven.six, name='six'),
    path('hostel/seven/7/', views.Hostel_seven.seven, name='seven'),


]
