from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.static import serve

from DrawMatch import settings
from .decorators.login_decorator import custom_login_required
from .decorators.logout_decorator import custom_logout_required
from .models import ActiveRooms


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
    username = request.user.name
    try:
        requestedRoom = ActiveRooms.objects.get(pk=room_code)
    except ActiveRooms.DoesNotExist:
        context = {
            'room_code': room_code,
            'username': username
        }
        return render(request, 'unfindable_room.html', context)

    user_id = request.user.id

    if requestedRoom.id_user_left and requestedRoom.id_user_left == user_id:
        user_direction = 'left'
    elif requestedRoom.id_user_right and requestedRoom.id_user_right == user_id:
        user_direction = 'right'
    elif requestedRoom.id_user_left is None:
        requestedRoom.id_user_left = user_id
        user_direction = 'left'
    elif requestedRoom.id_user_right is None and requestedRoom.id_user_left != user_id:
        requestedRoom.id_user_right = user_id
        user_direction = 'right'
    else:
        return HttpResponseNotFound('Room is full!')

    requestedRoom.save()

    context = {
        'room_code': room_code,
        'room': requestedRoom,
        'user_direction': user_direction,
        'user_id': user_id,
        'username': username
    }

    return render(request, 'room.html', context)


@custom_logout_required
def login(request):
    return render(request, 'login.html')


def handler404(request, exception):
    session_id = request.COOKIES.get('session_id')
    if session_id:
        if request.path.startswith('/room/'):
            room_code = request.path.split('/')[2]
            if room_code == '':
                return redirect('/')
            return redirect('room', room_code=room_code)
        else:
            return redirect('/')
    else:
        return redirect('/login/')
