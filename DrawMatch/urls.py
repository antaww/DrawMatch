from django.urls import path, re_path

from drawmatch_app import views
from drawmatch_app.ai_testing import draw_guess
from drawmatch_app.routes import create_room_route, register_route, login_route, logout_route, draw_route

urlpatterns = [
    # 404
    re_path('static/(?P<path>.*)$', views.serve_static),

    # Routes
    path('register-route', register_route.main),
    path('login-route', login_route.main),
    path('logout-route', logout_route.main),
    path('create-room-route', create_room_route.main),
    path('predict', draw_guess.main),
    path('store-drawing', draw_route.store_drawing),
    path('get-drawing', draw_route.get_drawing),
    path('generate-words', draw_route.generate_words),
    path('get-words', draw_route.get_words),
    path('remove-first-word', draw_route.remove_first_word),
    path('erase-drawing', draw_route.erase_drawing),
    path('add-score', draw_route.add_score),
    path('get-scores', draw_route.get_scores),

    # Pages
    path('login/', views.login),
    path('', views.home),
    path('room/<room_code>/', views.room, name='room'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]

handler404 = 'drawmatch_app.views.handler404'
