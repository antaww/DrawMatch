from django.urls import path, re_path

from drawmatch_app import views
from drawmatch_app.ai_testing import draw_guess
from drawmatch_app.routes import create_room_route, register_route

urlpatterns = [
    re_path('static/(?P<path>.*)$', views.serve_static),
    path('register', register_route.main),
    path('login/', views.login),
    path('', views.home),
    path('create-room/', create_room_route.main),
    path('join-room/', views.join_room),
    path('room/<room_code>/', views.room, name='room'),
    path('predict', draw_guess.main),
]

handler404 = 'drawmatch_app.views.handler404'
