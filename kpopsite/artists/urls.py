from django.urls import path
from . import views

urlpatterns = [
    path('', views.artists, name='artists_home'),

    path('boys-groups/', views.groups_boys, name='groups_boys'),
    path('girls-groups/', views.groups_girls, name='groups_girls'),
    path('mixed-groups/', views.groups_mix, name='groups_mix'),
    path('group/<slug:slug>/', views.group_info, name='group_info'), # /artists/group/bts/

    path('solo-male/', views.solo_m, name='solo_m'),
    path('solo-female/', views.solo_f, name='solo_f'),
    path('solo/<slug:slug>/', views.solo_info, name='solo_info'), # /artists/solo/agust-d/

    path('rating/', views.rating, name='rating'),
]