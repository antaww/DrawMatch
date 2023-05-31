from os import path

from django.shortcuts import redirect

from drawmatch_app import views
from drawmatch_app.models import ActiveRooms


def generate_room_code():
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def main(request):
    room_code = generate_room_code()
    while ActiveRooms.objects.filter(pk=room_code).exists():
        room_code = generate_room_code()
    ActiveRooms.objects.create(
        id=room_code,
        id_user_left_id=request.user.id,
        id_user_right_id=None
    )
    return redirect('room', room_code)
