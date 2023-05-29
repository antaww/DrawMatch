from django.urls import path
from drawmatch_app import views
from drawmatch_app.ai_testing import draw_guess

urlpatterns = [
    path('', views.home),
    path('create-room/', views.create_room),
    path('join-room/', views.join_room),
    path('room/<room_code>/', views.room),
    path('predict', draw_guess.main),
]
