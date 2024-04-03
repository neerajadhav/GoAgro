from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('home/', views.home, name='home'),
    path('liked/', views.like_unlike_post, name='liked'),
    path('newspaper/', views.newspaper, name='newspaper'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('notifications/', views.invited_received_view, name='notifications'),
    path('invite-profiles/', views.invite_profile_list_view, name='invite-profiles'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    # Add the URL pattern for the AJAX comment submission
    path('submit-comment/', views.submit_comment, name='submit-comment'),
]
