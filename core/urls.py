from django.urls import path
from . import views

urlpatterns = [
    path('',           views.home,             name='home'),
    path('register/',  views.register_view,    name='register'),
    path('login/',     views.login_view,       name='login'),
    path('logout/',    views.logout_view,      name='logout'),
    path('upload/',    views.upload_view,      name='upload'),
    path('tryon/',     views.try_on_view,      name='tryon'),
    path('save/',      views.save_outfit_view, name='save_outfit'),
    path('profile/',   views.profile_view,     name='profile'),
    path('trending/',  views.trending_view,    name='trending'),
]