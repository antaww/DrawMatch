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
    # Logique pour la page d'accueil
    return render(request, 'home.html')


@custom_login_required
def join_room(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        # Vérifier si le code du salon existe et gérer les redirections
        return redirect('room', room_code=room_code)
    return render(request, 'join_room.html')


@custom_login_required
def room(request, room_code):
    try:
        ActiveRooms.objects.get(pk=room_code)
    except ActiveRooms.DoesNotExist:
        return HttpResponseNotFound('Room does not exist!')  # todo: create 404 template

    context = {
        'room_code': room_code
    }
    return render(request, 'room.html', context)


@custom_logout_required
def login(request):
    return render(request, 'login.html')


def handler404(request, exception):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return redirect('/login/')
