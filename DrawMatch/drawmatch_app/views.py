from django.shortcuts import render, redirect
from .models import Room, Draw
from .forms import RoomForm


def home(request):
    # Logique pour la page d'accueil
    return render(request, 'drawmatch_app/home.html')


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
    return render(request, 'drawmatch_app/create_room.html', {'form': form})


def join_room(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        # Vérifier si le code du salon existe et gérer les redirections
        return redirect('room', room_code=room_code)
    return render(request, 'drawmatch_app/join_room.html')


def room(request, room_code):
    # Récupérer les informations du salon en utilisant le code
    # Gérer l'affichage des informations et des dessins associés au salon
    return render(request, 'drawmatch_app/room.html', {'room_code': room_code})


def draw(request, room_code):
    if request.method == 'POST':
        # Traiter le dessin soumis par l'utilisateur
        # Calculer le degré de correspondance avec l'IA
        # Enregistrer le dessin dans la base de données
        # Redirection ou affichage de résultats
        return redirect('room', room_code=room_code)
    return render(request, 'drawmatch_app/draw.html', {'room_code': room_code})
