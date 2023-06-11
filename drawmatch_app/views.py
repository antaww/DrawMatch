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
def join_room(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        return redirect('room', room_code=room_code)
    return render(request, 'join_room.html')


@custom_login_required
def room(request, room_code):
    try:
        requestedRoom = ActiveRooms.objects.get(pk=room_code)
    except ActiveRooms.DoesNotExist:
        return HttpResponseNotFound('Room does not exist!')  # todo: create 404 template

    user_id = request.user.id

    if requestedRoom.id_user_left and requestedRoom.id_user_left == user_id:
        user = 'left'
        context = {
            'room_code': room_code,
            'user': user
        }
        return render(request, 'room.html', context)
    elif requestedRoom.id_user_right and requestedRoom.id_user_right == user_id:
        user = 'right'
        context = {
            'room_code': room_code,
            'user': user
        }
        return render(request, 'room.html', context)
    elif requestedRoom.id_user_left is None:
        ActiveRooms.objects.filter(pk=room_code).update(id_user_left=user_id)
        user = 'left'
    elif requestedRoom.id_user_right is None and requestedRoom.id_user_left != user_id:
        ActiveRooms.objects.filter(pk=room_code).update(id_user_right=user_id)
        user = 'right'
    else:
        return HttpResponseNotFound('Room is full!')

    context = {
        'room_code': room_code,
        'user': user
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
            return redirect('room', room_code=room_code)
        else:
            return redirect('/')
    else:
        return redirect('/login/')
