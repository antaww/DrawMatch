from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import ActiveRooms


def home(request):
    # Logique pour la page d'accueil
    return render(request, 'home.html')


def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_code = form.cleaned_data['room_code']
            creator = request.user
            salon = Room.objects.create(code=room_code, createur=creator)
            # Autres traitements ou redirections
            return redirect('room', room_code=room_code)
    else:
        form = RoomForm()
    return render(request, 'create_room.html', {'form': form})


def join_room(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        # Vérifier si le code du salon existe et gérer les redirections
        return redirect('room', room_code=room_code)
    return render(request, 'join_room.html')


def room(request, room_code):
    try:
        ActiveRooms.objects.get(pk=room_code)
    except ActiveRooms.DoesNotExist:
        return HttpResponseNotFound('Room does not exist!')  # todo: create 404 template

    context = {
        'room_code': room_code
    }
    return render(request, 'room.html', context)
