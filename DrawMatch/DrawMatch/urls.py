from django.urls import path
from drawmatch_app import views
from drawmatch_app.ai_testing import draw_guess

urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('room/<str:room_code>/', views.room, name='room'),
    path('room/<str:room_code>/draw/', views.draw, name='draw'),
    path('predict', draw_guess.main, name='predict')
]
