
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns =[
    path('', HomePageView.as_view(), name='home'),
    path('my-courses', MyCoursesList.as_view(), name='my-courses'),
    path('course/<str:slug>', coursePage, name='coursepage'),
    path('check-out/<str:slug>', checkout, name='check-out'),
    path('verify_payment', verifyPayment, name='verify_payment'),
]