from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.static import serve

from DrawMatch import settings
from .decorators.login_decorator import custom_login_required
from .decorators.logout_decorator import custom_logout_required
from .models import ActiveRooms, Users, Points


def serve_static(request, path):
    return serve(request, path, document_root=settings.STATIC_ROOT)


@custom_login_required
def home(request):
    try:
        username = request.user.name
    except Exception as e:
        print(e)
    return render(request, 'home.html', {'username': username})


@custom_login_required
def room(request, room_code):
    user = Users.objects.get(pk=request.user.id)
    try:
        requestedRoom = ActiveRooms.objects.get(pk=room_code)
    except ActiveRooms.DoesNotExist:
        context = {
            'room_code': room_code,
            'username': user.name
        }
        return render(request, 'unfindable_room.html', context)

    if requestedRoom.id_user_left and requestedRoom.id_user_left.id == user.id:
        user_direction = 'left'
    elif requestedRoom.id_user_right and requestedRoom.id_user_right.id == user.id:
        user_direction = 'right'
    elif requestedRoom.id_user_left is None:
        requestedRoom.id_user_left = user
        user_direction = 'left'
    elif requestedRoom.id_user_right is None and requestedRoom.id_user_left.id != user.id:
        requestedRoom.id_user_right = user
        user_direction = 'right'
    else:
        return HttpResponseNotFound('Room is full!')

    requestedRoom.save()

    context = {
        'room_code': room_code,
        'room': requestedRoom,
        'user_direction': user_direction,
        'user_id': user.id,
    }

    return render(request, 'room.html', context)


@custom_logout_required
def login(request):
    return render(request, 'login.html')


@custom_login_required
def leaderboard(request):
    ordered_users = Points.objects.values(
        'user_id__name',
        'user_id'
    ).annotate(
        points_count=Sum('points')
    ).order_by('-points_count')

    user = Users.objects.get(pk=request.user.id)
    connected_user_points = Points.objects.filter(
        user_id=user
    ).aggregate(
        points_sum=Sum('points')
    )['points_sum']

    user_rank = 0
    for index, ordered_user in enumerate(ordered_users):
        if ordered_user['user_id'] == user.id:
            user_rank = index + 1
            break

    top_users = ordered_users[:5]

    context = {
        'users': top_users,
        'connected_user': user,
        'connected_user_rank': user_rank,
        'connected_user_points': connected_user_points,
    }
    return render(request, 'leaderboard.html', context)


def handler404(request, exception):
    session_id = request.COOKIES.get('session_id')
    if session_id:
        if request.path.startswith('/room/'):
            room_code = request.path.split('/')[2]
            if room_code == '':
                return redirect('/')
            return redirect('room', room_code=room_code)
        elif request.path == '/leaderboard':
            return redirect('leaderboard')
        else:
            return redirect('/')
    else:
        return redirect('/login/')
