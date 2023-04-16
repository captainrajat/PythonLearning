from django.urls import path

from . import views

urlpatterns = [
    path('', views.index1),
    path('xyz', views.index2),
    path('login', views.login),
    path('signup/',views.signup),
    path('v2/admin/location/states', views.getStates),
    path('v2/admin/location/districts/<str:id>/', views.getDistrict),
    path('shorturl', views.shorturl)
]