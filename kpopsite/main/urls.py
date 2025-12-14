from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),

    path('about_us', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('guide', views.guide, name='guide'),
    path('comebacks', views.comebacks, name='comebacks'),
    path('about_community', views.about_community, name='about_community'),
    path('what_is_kpop', views.what_is_kpop, name='what_is_kpop'),
    path('under_construction', views.under_construction, name='under_construction'),

    path('search/', views.search, name='search')
]
